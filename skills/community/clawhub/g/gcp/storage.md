# Storage — Cloud Storage, Disks, Filestore

Cloud Storage is cheap until a lifecycle rule meets a retrieval fee, and disks are cheap until nobody deletes them. Both failure modes are billing, not availability.

**Contents:** [Storage Classes and the Fee Nobody Reads](#storage-classes-and-the-fee-nobody-reads) · [Lifecycle Rules](#lifecycle-rules) · [Versioning Multiplies Everything](#versioning-multiplies-everything) · [Location Is Permanent](#location-is-permanent) · [Access Control](#access-control) · [Serving Content](#serving-content) · [Retention, Locks, and Deletion](#retention-locks-and-deletion) · [Persistent Disks and Hyperdisk](#persistent-disks-and-hyperdisk) · [Snapshots and Images](#snapshots-and-images) · [Filestore](#filestore) · [Moving Data In](#moving-data-in)

## Storage Classes and the Fee Nobody Reads

| Class | Storage price | Minimum storage duration | Retrieval fee |
|---|---|---|---|
| Standard | Highest | None | None |
| Nearline | Lower | 30 days | Per GB retrieved |
| Coldline | Lower still | 90 days | Higher per GB |
| Archive | Lowest | 365 days | Highest per GB |

Two charges make colder classes lose money for the wrong data:

- **Early deletion**: deleting, overwriting or transitioning an object before its minimum duration bills the remainder anyway. Moving an object to Archive and deleting it a month later costs a year of Archive storage.
- **Retrieval**: every read of a Nearline or colder object costs per GB, on top of the operation charge. Archive has no thaw delay — data is available immediately — but the fee applies every single time.

The break-even question is access frequency, not age. Data read monthly belongs in Standard even if it is five years old; data read once a year belongs in Coldline or Archive even if it is from last week. **Autoclass** moves objects between classes based on observed access, charges a management fee per object, and is the right default for a bucket whose access pattern is genuinely unknown — it removes the whole class of mistake above.

Operation charges are real at scale: listing and reading many small objects can cost more than storing them. A million tiny files is an operations bill wearing a storage costume; consider packing them.

## Lifecycle Rules

- Actions: delete, set storage class, abort incomplete multipart uploads. Conditions: age, creation date, number of newer versions, days since becoming noncurrent, current storage class, and a name prefix or suffix.
- **Rules evaluate asynchronously**, typically within a day. Do not build anything time-sensitive on the exact moment of execution.
- **Abort incomplete multipart uploads after 7 days.** Failed large uploads leave parts that are stored and billed and appear in no object listing. This is the most common invisible line item in a Cloud Storage bill, and one rule fixes it forever.
- **Test with a prefix first.** A lifecycle rule is applied to every matching object at once and deletions are not reversible unless versioning was already on.
- A rule that transitions to a colder class interacts with the minimum-duration charge: transitioning objects that will be deleted next month costs more than leaving them.

## Versioning Multiplies Everything

- With versioning on, an overwrite or delete keeps the old version, which is billed at full price. A bucket with churning objects and no noncurrent-version lifecycle rule grows without limit and nobody sees it in the object listing.
- The correct pairing is always both at once: **versioning on** *and* **a lifecycle rule deleting noncurrent versions after N days or beyond N newer versions**. Turning on the first without the second is how a 50 GB bucket bills as 2 TB.
- Soft delete retains deleted objects for a configurable window and is billed as storage during it. Useful protection; check the window against the bill, because on a high-churn bucket it is not free.

## Location Is Permanent

- A bucket's location is fixed at creation. Changing region means creating a new bucket and copying — with egress charges if it crosses regions.
- **Region vs dual-region vs multi-region**: multi-region gives geo-redundancy and higher availability at a higher storage price; a region is cheaper and keeps data in one place, which is what a residency requirement usually demands.
- Put the bucket where the compute is. A VM in one region reading a bucket in another pays inter-region egress on every byte, forever, and the misplacement is invisible in the console.
- Bucket names are globally unique across all of Google Cloud, and a deleted name is not immediately available for reuse. Name with a project or organization prefix.

## Access Control

- **Uniform bucket-level access** turns off per-object ACLs and makes IAM the only mechanism. Enable it on every bucket; ACLs are a second, invisible permission system that no audit script checks by default. It can be reverted only within a limited window after enabling, so decide at creation.
- **`constraints/storage.publicAccessPrevention`** enforced at the org node makes a public bucket impossible. This is the control that stops the classic leak, and it is free.
- **`allUsers`** means the whole internet. **`allAuthenticatedUsers`** means anyone with a Google account, anywhere — it is not "our users", and it is the more dangerous of the two because it sounds restricted.
- **Signed URLs** grant time-limited access to a single object without any IAM change. Sign them using the service account's signBlob permission rather than a downloaded key (`iam.md`), and keep the expiry short.
- **HMAC keys** exist for S3-compatible clients. They are long-lived credentials attached to a service account — treat them exactly like service account keys and prefer not to have them.
- IAM Conditions on bucket bindings can restrict a role to an object-name prefix, which is how one bucket serves several teams without one team reading another's data.

## Serving Content

- Public web content: a bucket behind an external Application Load Balancer with Cloud CDN, not a public bucket. The load balancer brings TLS with a managed certificate, custom domains, Cloud Armor, and caching. A public bucket gives none of it and cannot be protected later without changing the URL (`networking.md`).
- Cache keys include the query string by default. A cache-busting parameter that changes per request produces a 0% hit rate and full origin cost.
- Set `Cache-Control` on objects at upload. Objects with no cache header get conservative defaults and the CDN does much less than the bill suggests it should.
- For user uploads, hand out a signed URL and let the client upload directly to the bucket. Proxying uploads through Cloud Run burns request time, memory and instance count for no benefit (`run.md`).

## Retention, Locks, and Deletion

- **Retention policy** on a bucket prevents deletion of objects younger than the retention period. **Locking** it makes the policy permanent — the bucket can never have its retention shortened and objects can never be deleted early, by anyone, including the org admin.
- Lock only when a regulation requires it. A locked retention policy on a bucket that also receives ordinary data means paying to store that data for the full period with no way out.
- **Object holds** are a per-object equivalent, useful for a legal hold on specific data.
- Deleting a bucket requires it to be empty, which for a versioned bucket means every version. Lifecycle rules are how you get there.

## Persistent Disks and Hyperdisk

- **Billed on provisioned size, not used.** A 500 GB disk that holds 20 GB costs 500 GB every month.
- Types, cheapest to most expensive: standard (HDD), balanced (SSD, the correct default), SSD (higher IOPS), extreme / Hyperdisk (provisioned IOPS and throughput billed separately from capacity). **Hyperdisk decouples performance from size**, which removes the old trick of over-provisioning capacity to buy IOPS — check whether the workload's disk is oversized for that reason.
- On the older types, IOPS scale with size and with the instance's machine type. A small disk on a large VM and a large disk on a small VM are both bottlenecked; check both before concluding the disk is slow.
- Disks can grow online and **can never shrink**. Shrinking means creating a smaller disk and copying.
- **`auto-delete` is set at attach time.** Without it, deleting the VM leaves the disk behind, billed forever, attached to nothing. This is the most common orphaned resource in a GCP project — the idle-disk Recommender finds them (`costs.md`).
- Regional persistent disks synchronously replicate across two zones and roughly double the cost. They are the mechanism behind a zonal-failure-tolerant stateful VM, and they are not a backup.
- Local SSD is physically attached, fast, and **erased when the VM stops**. It is scratch space; anything on it is gone after a live migration or a stop.

## Snapshots and Images

- Snapshots are incremental after the first, but the chain retains the blocks: deleting an intermediate snapshot does not necessarily free its data, because later snapshots may still reference it. A long chain with no retention policy grows quietly.
- Use a **snapshot schedule with a retention policy** attached to the disk. It is the only version of this that stays correct without a human.
- Snapshots are global resources and can be restored into another region — which is the cheap half of a cross-region DR story.
- **Machine images** capture the whole VM (all disks, metadata, machine config) and are the right primitive for cloning a configured instance; a disk snapshot is not.
- Test a restore, do not assume one. Record the measured restore time in `deploys/<year>.md` under `## Restore Drills` (`production.md`).

## Filestore

- Managed NFS, priced by provisioned capacity per hour with a substantial minimum per tier. It bills continuously from creation.
- Choose it only when a workload genuinely needs POSIX shared file semantics — lift-and-shift applications, some ML training data layouts, shared scratch for a rendering pipeline.
- For everything else, Cloud Storage with a client library is cheaper by an order of magnitude. Mounting a bucket as a filesystem (FUSE-style) is convenient and has very different latency and consistency characteristics from a real NFS mount; it is fine for read-mostly access to large objects and bad for small random writes.

## Moving Data In

| Volume / source | Tool |
|---|---|
| Small, ad hoc | The CLI's storage commands (which replaced the older `gsutil` tooling and are substantially faster on many small files) |
| Another cloud, or a public URL, on a schedule | Storage Transfer Service — managed, resumable, no VM to babysit |
| On-premises, large | Storage Transfer Service agents, or a physical transfer appliance when the network math says months |
| Continuous from a database | Datastream (`pipelines.md`) |

Parallel composite uploads speed up large single files and produce an object whose checksum behaves differently — fine for data, a surprise for anything verifying an MD5. Always transfer with checksums enabled and verify counts at the end; a transfer that silently skipped 3% is worse than one that failed.

When a bucket, disk layout or lifecycle policy is created or changed, update `## Current Infrastructure` in `~/Clawic/data/gcp/memory.md`, and record any resulting saving in `### Optimization Log` with its monthly value — otherwise the same orphaned-disk sweep gets rediscovered next quarter (`memory-template.md`).

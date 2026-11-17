# Troubleshooting

Common first-run failures and how to read them. For the diagnostic command
itself, see `nodo doctor` in [`USAGE.md`](./USAGE.md); for packing errors see the
*Common Issues and Solutions* section of [`PACKING.md`](./PACKING.md).

## Architecture mismatch (most common packing failure)

**Symptom:** `nodo pack` (or an execute of a freshly packed service) fails early
with an explicit architecture/unsupported-architecture message.

**Why:** this install profile **disables cross-arch builds** and **does not
install QEMU/binfmt** (see *Operational notes* in [`INSTALL.md`](./INSTALL.md)). A
service's `service.json → architecture` (e.g. `linux/amd64`, `linux/arm64`) must
match the host running the packer.

**Fix:**
- Set `service.json → architecture` to your host's architecture (`uname -m` →
  `x86_64` = `linux/amd64`, `aarch64` = `linux/arm64`). See
  [`PACKING.md`](./PACKING.md) → *architecture*.
- Or pack on a host of the target architecture.
- `packer.ARM_PACKER_SUPPORT` / `packer.X86_PACKER_SUPPORT` in `config.yaml`
  control which architectures the packer will accept/announce.

## KVM unavailable (services won't execute)

**Symptom:** `nodo execute` fails to launch a microVM; `nodo doctor` reports no
`/dev/kvm`, missing KVM modules, or a failed KVM smoke test.

**Why:** services run as Cloud Hypervisor microVMs, which need hardware
virtualization (`/dev/kvm`). It is commonly unavailable when:
- CPU virtualization (VT-x/`vmx`, AMD-V/`svm`) is disabled in BIOS/UEFI.
- Running inside a VM without **nested virtualization** enabled.
- Running inside an unprivileged container without `/dev/kvm` passed through.
- On WSL2 — see [`WSL.md`](https://github.com/celaut-project/nodo/blob/stable/docs/WSL.md) for the mirrored-networking / KVM setup.

**Fix — run `sudo nodo doctor` and read its checks:**
- **CPU virtualization flags (`vmx`/`svm`)** — if absent, enable virtualization in
  firmware, or enable nested virt on the parent hypervisor.
- **KVM modules and `/dev/kvm` access** — load `kvm` + `kvm_intel`/`kvm_amd`;
  ensure the nodo user can access `/dev/kvm`.
- **Cloud Hypervisor binary existence and version** — reinstall CH assets
  ([`INSTALL.md`](./INSTALL.md) step 10) if missing.
- **Guest kernel (`vmlinuz`) / initramfs presence** — the guest kernel must
  exist and be ≥1 MiB; the initramfs must exist and contain `init`,
  `bin/busybox`, and the `etc/nodo-ch-initramfs.marker` marker (verified with
  `lsinitramfs`). To rebuild the initramfs, re-run the installer, or invoke the
  builder with its positional arguments, e.g.
  `sudo bash /nodo/bash/build_ch_initramfs.sh /nodo linux/amd64 /nodo/cloud_hypervisor/initramfs/linux/amd64/initramfs`.
- **KVM smoke test** — launches a minimal VM; a failure here means CH cannot
  execute vCPUs on this kernel even though the earlier checks passed (often a
  container/nested-virt limitation, or a bleeding-edge host kernel that `doctor`
  warns about).

`doctor` also checks/repairs the `nodo.service` systemd unit; run it with `sudo`.

## KyA prompt blocks automation

**Symptom:** a headless/agent run hangs or exits at the Know Your Assumptions
`yes/no` prompt.

**Fix:** pre-accept by creating the marker file (only in environments you
control) — `mkdir -p /nodo/storage && touch /nodo/storage/.acceptedkya`. See
[`USAGE.md`](./USAGE.md#non-interactive-use-automation--agents-️) and
[`KyA.md`](./KyA.md).

## Payment / reputation features error out

**Symptom:** `nodo info` or payment/reputation actions report a Java dependency
missing.

**Why:** Java is **optional** and only required for Ergo-backed payment and
reputation features ([`INSTALL.md`](./INSTALL.md)). Core install/pack/execute work
without it.

**Fix:** install the local JRE (INSTALL.md step 7), or avoid the payment/
reputation commands. Also ensure `ledgers.ergo.WALLET_MNEMONIC` is set if you
intend to pay or submit reputation (see [`CONFIG.md`](./CONFIG.md)).

## `nodo pack` can't find a packer

**Symptom:** default-mode pack fails to resolve a packer-service.

**Why/Fix:** in default mode (`packer.local: false`) you must set the packer's
published id under `core_services` in `config.yaml` and have a running instance
(`nodo execute <packer-service id>`). Alternatively set
`packer.PACKER_SERVICE_URL` to an out-of-band packer, or set `packer.local: true`
to build locally. See [`CONFIG.md`](./CONFIG.md) and [`INSTALL.md`](./INSTALL.md)
step 9.

## Uninstalling

There is a full uninstall path — automatic (`uninstall.sh`) and manual. See
[`UNINSTALL.md`](./UNINSTALL.md).

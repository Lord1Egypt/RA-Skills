# Fly/Tigris Object Storage Documentation

## Source

- Canonical URL: https://fly.io/docs/tigris/
- Related URL: https://www.tigrisdata.com/docs/overview/
- Related URL: https://www.tigrisdata.com/docs/concepts/architecture/

## Summary

Fly's Tigris integration is a useful reference for the storage side of a knowledge system because it combines an S3-compatible API with a globally caching delivery model. In practical terms, Tigris lets you keep object storage behind familiar S3 semantics while taking advantage of Fly's global network for lower-latency access. That combination fits well with use cases where a knowledge repo needs to publish mirrored documentation, generated wiki snapshots, or other static artifacts to readers and agents in different regions.

The most important conceptual detail is how objects are stored and cached. Tigris documentation explains that objects are served close to the requesting user and that subsequent requests are cached in the user's region. With shadow buckets, Tigris can also front an existing S3-compatible store: if an object is missing locally, it can fetch from the shadow bucket, store it in a nearby region, and then serve future reads from Tigris. That makes Tigris not just storage, but also a migration and mirroring layer.

The public-versus-private bucket distinction is intentionally simple. Buckets are private by default, and a bucket can be made public for unauthenticated asset access. Public content is served from dedicated domains, while private access stays behind authentication and signed access patterns. The docs also note that bucket visibility is bucket-wide rather than ACL-driven, which keeps the mental model cleaner for operational use.

Fly CLI integration matters because it keeps storage management in the same operational workflow as the rest of Fly infrastructure. Commands like `fly storage create --public`, `flyctl storage list`, `flyctl storage dashboard`, and shadow bucket configuration make the storage layer scriptable and automatable. For this repository, the most relevant use case is publishing or mirroring knowledge artifacts: wiki snapshots, imported documentation, or static exports can live in a globally cached bucket while the repo remains the canonical authoring source.

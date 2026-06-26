# Vendored client assets

| File | Source | Version | License |
|---|---|---|---|
| echarts.min.js | https://github.com/apache/echarts | 5.5.0 | Apache-2.0 |

Vendored so the local Web UI dashboard works fully offline and avoids
leaking a request hint (IP / User-Agent) to a third-party CDN.

## Upgrade procedure

1. `npm view echarts@<version> dist.shasum` to grab the published shasum.
2. `npm view echarts@<version> dist.tarball` to grab the tarball URL.
3. Download tarball, verify shasum, extract `package/dist/echarts.min.js`.
4. Replace the file here, bump the table above, run `node --test test/webui*.test.js`.

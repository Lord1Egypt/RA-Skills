---
name: draco3d
description: Google Draco 3D geometry compression library. Compresses and decompresses 3D meshes and point clouds, with glTF, Three.js, and Unity integration.
---

# Draco3D — 3D Geometry Compression

`npm i draco3d` (WASM codec) | CDN: `gstatic.com/draco/versioned/decoders/1.5.7/`

## Use Cases

Use when compressing 3D models, decoding Draco files, integrating Draco in web projects, using the draco3d npm package, or handling glTF Draco extensions.

## Decoding

```js
import DracoDecoderModule from 'draco3d/draco_decoder.js';
const d = await DracoDecoderModule();

const buf = new d.DecoderBuffer();
buf.Init(bytes, bytes.length);
const dec = new d.Decoder();
const type = dec.GetEncodedGeometryType(buf);

const geo = type === d.TRIANGULAR_MESH ? new d.Mesh() : new d.PointCloud();
type === d.TRIANGULAR_MESH
  ? dec.DecodeBufferToMesh(buf, geo)
  : dec.DecodeBufferToPointCloud(buf, geo);

// Read positions
const a = dec.GetAttribute(geo, d.POSITION);
const fa = new d.DracoFloat32Array();
dec.GetAttributeFloatForAllPoints(geo, a, fa);

// Read face indices (mesh only)
const ia = new d.DracoInt32Array();
for (let i = 0; i < geo.num_faces(); i++) {
  dec.GetFaceFromMesh(geo, i, ia); // ia.GetValue(0/1/2)
}

// ⚠️ Must manually release
d.destroy(geo); d.destroy(dec); d.destroy(buf); d.destroy(fa);
```

## Encoding

```js
import DracoEncoderModule from 'draco3d/draco_encoder.js';
const d = await DracoEncoderModule();

const mesh = new d.Mesh();
const b = new d.MeshBuilder();
b.AddFacesToMesh(mesh, numFaces, indices);
b.AddFloatAttributeToMesh(mesh, d.POSITION, numVerts, 3, positions);
b.AddFloatAttributeToMesh(mesh, d.NORMAL, numVerts, 3, normals);

const enc = new d.Encoder();
enc.SetEncodingMethod(d.MESH_EDGEBREAKER_ENCODING);
enc.SetAttributeQuantization(d.POSITION, 11);

const out = new d.DracoInt8Array();
enc.EncodeMeshToDracoBuffer(mesh, out);
d.destroy(mesh); d.destroy(enc); d.destroy(b);
```

## Three.js

```js
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader.js';
const loader = new DRACOLoader();
loader.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.7/');
gltfLoader.setDRACOLoader(loader);
```

## Attribute Constants & Quantization Defaults

| Constant | Quant. Bits | Range |
|----------|-------------|-------|
| `POSITION` | 11 | 8–14 |
| `NORMAL` | 7 | 6–10 |
| `TEX_COORD` | 10 | 8–12 |
| `COLOR` | 8 | 6–10 |
| `GENERIC` | 8 | — |

Encoding methods: `MESH_EDGEBREAKER_ENCODING` (high compression, default) | `MESH_SEQUENTIAL_ENCODING` (faster decode)

## Key Notes

- Module returns a Promise — **must await**
- All WASM objects **must be released via `d.destroy(obj)`**, otherwise memory leaks
- Production: **lock CDN version**, avoid the unversioned `/v1/decoders/` path

## Detailed API

[references/api-reference.md](references/api-reference.md) — Decoder/Encoder/MeshBuilder full method signatures, Metadata, ExpertEncoder, Node.js.
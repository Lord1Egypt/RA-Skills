# Draco3D API Reference

## Decoder

```js
const d = await DracoDecoderModule();

// Buffer
const buf = new d.DecoderBuffer();
buf.Init(data, data.length);

// Decode
const dec = new d.Decoder();
const type = dec.GetEncodedGeometryType(buf); // TRIANGULAR_MESH | POINT_CLOUD | INVALID_GEOMETRY_TYPE
const geo = type === d.TRIANGULAR_MESH ? new d.Mesh() : new d.PointCloud();
type === d.TRIANGULAR_MESH ? dec.DecodeBufferToMesh(buf, geo) : dec.DecodeBufferToPointCloud(buf, geo);

// Read attributes
const attr = dec.GetAttribute(geo, d.POSITION); // or GetAttributeByUniqueId(geo, id)
const fa = new d.DracoFloat32Array();
dec.GetAttributeFloatForAllPoints(geo, attr, fa); // batch
dec.GetAttributeFloatForPoint(geo, attr, i, out); // per-point

// Face indices
const ia = new d.DracoInt32Array();
for (let i = 0; i < geo.num_faces(); i++) { dec.GetFaceFromMesh(geo, i, ia); }

// Meta
geo.num_points(); geo.num_attributes();
attr.unique_id(); attr.attribute_type(); attr.data_type(); attr.num_components(); attr.normalized();
```

## Encoder

```js
const d = await DracoEncoderModule();

const enc = new d.Encoder();
enc.SetEncodingMethod(d.MESH_EDGEBREAKER_ENCODING); // or MESH_SEQUENTIAL_ENCODING
enc.SetAttributeQuantization(d.POSITION, 11);
enc.SetSpeedOptions(7, 7); // (encSpeed, decSpeed) 0-10

// MeshBuilder
const mesh = new d.Mesh();
const b = new d.MeshBuilder();
b.AddFacesToMesh(mesh, nFaces, indices);
b.AddFloatAttributeToMesh(mesh, d.POSITION, nPts, 3, data);
b.AddIntAttributeToMesh(mesh, attrType, nPts, comp, data);
b.AddUInt8AttributeToMesh(mesh, attrType, nPts, comp, data);

// Output
const out = new d.DracoInt8Array();
enc.EncodeMeshToDracoBuffer(mesh, out);
```

## ExpertEncoder

```js
const ee = new d.ExpertEncoder(mesh);
ee.SetAttributeQuantization(attrId, bits);
ee.SetSkipAttributeTransform(attrId);
ee.EncodeToDracoBuffer(false, out);
```

## Point Cloud

```js
const b = new d.PointCloudBuilder();
const pc = new d.PointCloud();
b.AddFloatAttribute(pc, d.POSITION, nPts, 3, pos);
enc.EncodePointCloudToDracoBuffer(pc, false, out);
```

## Metadata

```js
const md = dec.GetMetadata(geo);
for (let i = 0; i < md.num_entries(); i++) { md.GetEntryName(i); md.GetEntryValue(i); }
dec.GetAttributeMetadata(geo, attr);
```

## Node.js

```js
const draco3d = require('draco3d');
const dec = await draco3d.createDecoderModule();
const enc = await draco3d.createEncoderModule();
// API same as browser
```

## Data Type Constants

`DT_INT8` `DT_UINT8` `DT_INT16` `DT_UINT16` `DT_INT32` `DT_UINT32` `DT_FLOAT32` `DT_FLOAT64`

## Memory

All Module-created objects must be released via `d.destroy(obj)`, otherwise WASM memory leaks.
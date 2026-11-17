---
name: face-api
description: Build face detection, face landmark detection, face recognition, face expression (emotion) recognition, and age/gender estimation with the face-api.js library (browser or Node.js). 
---

# face-api.js

Face detection/recognition on top of TensorFlow.js core. Browser (WebGL) or Node.js (`@tensorflow/tfjs-node` + `canvas` polyfills).

## Use Cases

Use when detecting faces in images/video/webcam, drawing bounding boxes or 68-point landmarks, computing/matching 128-d face descriptors via FaceMatcher, classifying facial expressions, estimating age/gender, or realtime face tracking. Covers model selection (SSD Mobilenet v1, Tiny Face Detector, MTCNN), model loading, and the detectAllFaces/detectSingleFace chained API.

## What it does

Face detection (3 detectors), 68-point landmarks, 128-d descriptor recognition via `FaceMatcher`, 7-expression classification, and age/gender estimation. Draw boxes/landmarks/expression bars to canvas; realtime webcam tracking.

## Decide first

Pick the detector, then chain the signals you need. Model details (sizes, accuracy, exact filenames, download) → [references/models.md](references/models.md).

| Need | Detector / model |
|------|------------------|
| Realtime / mobile / webcam | Tiny Face Detector (`tiny_face_detector_model`) |
| Accurate boxes (the default) | SSD Mobilenet v1 (`ssd_mobilenetv1_model`) |
| 5-point landmarks + scale control | MTCNN (`mtcnn_model`) |
| Landmarks | `face_landmark_68_model` / `_tiny` |
| Identity | `face_recognition_model` (128-d) |
| Emotion | `face_expression_model` |
| Age & gender | `age_gender_model` |

## Quick start

Browser: `npm i face-api.js`. Node: `npm i face-api.js canvas @tensorflow/tfjs-node`, then `faceapi.env.monkeyPatch({ Canvas, Image, ImageData })` (from `canvas`, required before any detection).

Load models once — manifest + shards must sit in the **same directory**:

```js
await faceapi.loadSsdMobilenetv1Model('/models')   // or faceapi.nets.ssdMobilenetv1.loadFromUri('/models')
await faceapi.loadFaceLandmarkModel('/models')
await faceapi.loadFaceRecognitionModel('/models')
```

## Core API

```js
const results = await faceapi
  .detectAllFaces(input)     // or detectSingleFace(input)
  .withFaceLandmarks()       // 68 points
  .withFaceDescriptors();    // 128-d Float32Array
```

Chain methods: `.withFaceLandmarks(useTinyModel?)` · `.withFaceDescriptor()/.withFaceDescriptors()` · `.withFaceExpressions()` · `.withAgeAndGender()`.

- **Recognition:** `new faceapi.FaceMatcher(refs).findBestMatch(q.descriptor)` → `{ label, distance }` (threshold 0.6).
- **Draw:** `faceapi.matchDimensions(canvas, size)` + `faceapi.resizeResults(results, size)` + `faceapi.draw.drawDetections/.drawFaceLandmarks/.drawFaceExpressions`.

Runnable examples → [references/examples.md](references/examples.md). Full API → [references/api-reference.md](references/api-reference.md).

## Gotchas

- Manifest + shard files must live in the **same directory** or loading fails.
- Node **requires** `monkeyPatch({ Canvas, Image, ImageData })` first; MTCNN also needs `ImageData`.
- **No TS types** in v0.22.2 (and no `@types/face-api.js`): add a `declare module` shim, use `any`, or use the maintained `@vladmandic/face-api` fork (types + CDN models).
- Pins old `@tensorflow/tfjs-core` 1.7.x — don't mix newer tfjs.
- First inference is slow (warm-up); wrap realtime loops in `tf.tidy()`.
- **Docs are stale:** old `drawDetection`/`drawLandmarks`/`BoxWithText` → use `faceapi.draw.drawDetections`/`.drawFaceLandmarks`/`.DrawTextField`.

# Models Reference

All models live in the repo's [`weights/`](https://github.com/justadudewhohacks/face-api.js/tree/master/weights) directory. Each model is a `*-weights_manifest.json` plus one or more `*-shardN` binary files. **Keep the manifest and its shards in the same directory / same URL route**, and serve/load from that directory.

## Downloading weights

The simplest path: clone the repo or download the `weights/` folder and copy the models you need into `public/models` (browser) or `./models` (Node).

```bash
# shallow clone, then copy the weights dir you need
git clone --depth 1 https://github.com/justadudewhohacks/face-api.js
cp -r face-api.js/weights ./models
```

Each model folder must contain its manifest + all shards.

> **Maintained fork:** `@vladmandic/face-api` actively maintains face-api.js — it ships TypeScript types, updates the tfjs dependency, and hosts the model weights on a CDN (`https://cdn.jsdelivr.net/npm/@vladmandic/face-api/model/`). Prefer it for new TypeScript projects; this skill's API references still apply (near-identical surface).

## Face detection models

### SSD Mobilenet v1 (`ssd_mobilenetv1_model`)

- **Size:** ~5.4 MB quantized (`shard1` + `shard2`)
- **Role:** default detector for `detectAllFaces` / `detectSingleFace`.
- **Accuracy vs speed:** aims for high bounding-box accuracy, not low inference time.
- **Trained on:** WIDERFACE dataset; weights from [yeephycho](https://github.com/yeephycho/tensorflow-face-detection).
- **Options:** `SsdMobilenetv1Options` (`minConfidence` 0.5, `maxResults` 100).
- **Use when:** you want the most reliable boxes and can afford size/latency.

### Tiny Face Detector (`tiny_face_detector_model`)

- **Size:** ~190 KB quantized (`shard1`)
- **Role:** **go-to for mobile / resource-limited clients and realtime webcam.**
- **Tradeoff:** much faster/smaller than SSD, slightly worse on small faces.
- **Notes:** boxes fully cover facial feature points → pairs well with landmark detection. A tinier Tiny Yolo V2 with depthwise-separable convolutions; fully convolutional, adapts to different `inputSize` (must be divisible by 32).
- **Options:** `TinyFaceDetectorOptions` (`inputSize` 416, `scoreThreshold` 0.5).

### MTCNN (`mtcnn_model`)

- **Size:** ~2 MB (`shard1`)
- **Role:** alternative; 3-stage cascaded CNN. Mostly kept for experimentation.
- **Key feature:** returns **5 face landmark points** (`FaceLandmarks5`) alongside boxes + scores, and offers the most configuration room (scale pyramid).
- **Options:** `MtcnnOptions` (`minFaceSize` 20, `scoreThresholds` [0.6,0.7,0.7], `scaleFactor` 0.709, `maxNumScales` 10, or explicit `scaleSteps`).
- **Note:** needs the `ImageData` polyfill in Node.js. `FaceLandmarks5` has no contour getters (`getNose()` etc.) — those are 68-point only.

## 68-point face landmark models

### `face_landmark_68_model` (default, ~350 KB) / `face_landmark_68_tiny_model` (~80 KB)

- Lightweight, fast, accurate 68-point landmark detector (eyes, brows, nose, mouth, jawline).
- Depthwise-separable convs + densely-connected blocks; trained on ~35k face images.
- **Use tiny model** for speed/size when landmarks only need to be approximate.
- Chain with `.withFaceLandmarks(/* useTinyModel */ true)`.

## Face recognition model (`face_recognition_model`)

- **Size:** ~6.2 MB (`shard1` + `shard1`; two shards)
- **Role:** compute a **128-d face descriptor** (Float32Array) — the "identity fingerprint".
- **Architecture:** ResNet-34-like; equivalent to dlib's FaceRecognizerNet. **99.38% on LFW**.
- **Key property:** not limited to training identities — descriptors work for any face; compare any two faces by euclidean distance.
- Chain with `.withFaceDescriptors()` / `.withFaceDescriptor()`.

## Face expression model (`face_expression_model`)

- **Size:** ~310 KB (`shard1`)
- **Role:** classify 7 expressions: `neutral | happy | sad | angry | fearful | disgusted | surprised`.
- **Caveat:** accuracy drops if the subject wears glasses.
- Chain with `.withFaceExpressions()`; result is a `FaceExpressions` object (use `.asSortedArray()`).

## Age & gender model (`age_gender_model`)

- **Size:** ~420 KB (`shard1`)
- **Role:** estimate age + classify gender in one multitask net (feature extractor + age regression head + gender classifier).
- **Accuracy:** MAE (mean age error) **4.54**; gender accuracy **95%**.
- Chain with `.withAgeAndGender()`; adds `age` (number) and `gender` (`'male' | 'female'`) + `genderProbability`.

## Model registry (`faceapi.nets`)

All singleton instances, loaded once then reused:

```js
faceapi.nets.ssdMobilenetv1
faceapi.nets.tinyFaceDetector
faceapi.nets.tinyYolov2
faceapi.nets.mtcnn
faceapi.nets.faceLandmark68Net
faceapi.nets.faceLandmark68TinyNet
faceapi.nets.faceRecognitionNet
faceapi.nets.faceExpressionNet
faceapi.nets.ageGenderNet
```

## Loading a model — equivalent forms

```js
// canonical: explicit load target (recommended)
await faceapi.nets.ssdMobilenetv1.loadFromUri('/models');     // browser URL
await faceapi.nets.ssdMobilenetv1.loadFromDisk('./models');   // Node.js path
await faceapi.nets.ssdMobilenetv1.loadFromWeightMap(weightMap);

// convenience loaders (call net.load(url) — environment-aware)
await faceapi.loadSsdMobilenetv1Model('/models');
await faceapi.loadTinyFaceDetectorModel('/models');
await faceapi.loadMtcnnModel('/models');
await faceapi.loadTinyYolov2Model('/models');
await faceapi.loadFaceLandmarkModel('/models');
await faceapi.loadFaceLandmarkTinyModel('/models');
await faceapi.loadFaceRecognitionModel('/models');
await faceapi.loadFaceExpressionModel('/models');
await faceapi.loadAgeGenderModel('/models');

// aliases (backward compatibility)
faceapi.loadFaceDetectionModel === faceapi.loadSsdMobilenetv1Model

// own instance
const net = new faceapi.SsdMobilenetv1();
await net.loadFromUri('/models');

// raw Float32Array weights (uncompressed model)
net.load(await faceapi.fetchNetWeights('/models/ssd_mobilenetv1_model.weights'));
```
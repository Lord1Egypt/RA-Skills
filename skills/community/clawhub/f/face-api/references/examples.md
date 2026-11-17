# Examples

Complete, runnable patterns. Assume models are in `public/models` (browser) or `./models` (Node).

## 1. Browser — full pipeline (detect + landmarks + descriptors)

```html
<img id="inputImg" src="images/group.jpg" />
<canvas id="overlay" />
```

```js
import * as faceapi from 'face-api.js';

const MODEL_URL = '/models';
const input = document.getElementById('inputImg');
const overlay = document.getElementById('overlay');

async function init() {
  await Promise.all([
    faceapi.loadSsdMobilenetv1Model(MODEL_URL),
    faceapi.loadFaceLandmarkModel(MODEL_URL),
    faceapi.loadFaceRecognitionModel(MODEL_URL),
  ]);
  return run();
}

async function run() {
  const results = await faceapi
    .detectAllFaces(input)
    .withFaceLandmarks()
    .withFaceDescriptors();

  // draw at display size
  const displaySize = { width: input.width, height: input.height };
  faceapi.matchDimensions(overlay, displaySize);          // sets canvas size
  const sized = faceapi.resizeResults(results, displaySize);
  faceapi.draw.drawDetections(overlay, sized);
  faceapi.draw.drawFaceLandmarks(overlay, sized);
}

init();
```

## 2. Browser — face recognition with FaceMatcher

```js
// build reference set once
const refs = await faceapi
  .detectAllFaces(refImage)
  .withFaceLandmarks()
  .withFaceDescriptors();

const faceMatcher = new faceapi.FaceMatcher(refs, 0.6);

// recognize a query
const res = await faceapi
  .detectSingleFace(queryImage)
  .withFaceLandmarks()
  .withFaceDescriptor();

if (res) {
  const best = faceMatcher.findBestMatch(res.descriptor);
  console.log(best.toString()); // "person 1 (0.34)"
  // draw the label
  new faceapi.draw.DrawTextField(
    [`${best.label} (${best.distance.toFixed(2)})`],
    res.detection.box.bottomLeft
  ).draw(overlay);
}
```

Labeled references:

```js
const faceMatcher = new faceapi.FaceMatcher([
  new faceapi.LabeledFaceDescriptors('alice', [aliceDesc1, aliceDesc2]),
  new faceapi.LabeledFaceDescriptors('bob', [bobDesc]),
]);
```

## 3. Browser — realtime webcam tracking (Tiny Face Detector)

```html
<video id="video" autoplay muted playsinline></video>
```

```js
const video = document.getElementById('video');

async function start() {
  await Promise.all([
    faceapi.loadTinyFaceDetectorModel(MODEL_URL),
    faceapi.loadFaceLandmarkTinyModel(MODEL_URL),
    faceapi.loadFaceExpressionModel(MODEL_URL),
  ]);

  const stream = await navigator.mediaDevices.getUserMedia({ video: {} });
  video.srcObject = stream;

  setInterval(async () => {
    const results = await faceapi
      .detectAllFaces(video, new faceapi.TinyFaceDetectorOptions({ inputSize: 160, scoreThreshold: 0.5 }))
      .withFaceLandmarks(true)
      .withFaceExpressions();

    // draw onto a canvas sized to video
    faceapi.draw.drawDetections(canvas, results);
    faceapi.draw.drawFaceExpressions(canvas, results);
  }, 100);
}
```

## 4. Browser — expression recognition

```js
const results = await faceapi
  .detectAllFaces(input)
  .withFaceLandmarks()
  .withFaceExpressions();

results.forEach(({ detection, expressions }) => {
  // expressions is a FaceExpressions object; asSortedArray() → desc by probability
  const { expression, probability } = expressions.asSortedArray()[0];
  console.log(`face @ ${detection.box}: ${expression} (${(probability * 100).toFixed(1)}%)`);
});
```

## 5. Browser — age & gender estimation

```js
await faceapi.loadAgeGenderModel(MODEL_URL);

const results = await faceapi
  .detectAllFaces(input)
  .withFaceLandmarks()
  .withAgeAndGender();

results.forEach(({ detection, age, gender, genderProbability }) => {
  console.log(`face @ ${detection.box}: ${gender} (${(genderProbability * 100).toFixed(1)}%), ~${Math.round(age)}yo`);
});
```

## 6. Node.js — pipeline on a local image file

```js
import '@tensorflow/tfjs-node';
import * as canvas from 'canvas';
import * as faceapi from 'face-api.js';
import * as fs from 'fs';

const { Canvas, Image, ImageData } = canvas;
faceapi.env.monkeyPatch({ Canvas, Image, ImageData });

async function main() {
  await faceapi.nets.ssdMobilenetv1.loadFromDisk('./models');
  await faceapi.nets.faceLandmark68Net.loadFromDisk('./models');
  await faceapi.nets.faceRecognitionNet.loadFromDisk('./models');

  const img = await canvas.loadImage('./images/test.jpg');
  const detections = await faceapi
    .detectAllFaces(img)
    .withFaceLandmarks()
    .withFaceDescriptors();

  detections.forEach((d) => {
    console.log('box:', d.detection.box, 'score:', d.detection.score);
    console.log('descriptor length:', d.descriptor.length); // 128
  });
}

main().catch(console.error);
```

## 7. Node.js — compare two faces (similarity)

```js
const [a, b] = await Promise.all([
  faceapi.detectSingleFace(await canvas.loadImage('a.jpg')).withFaceLandmarks().withFaceDescriptor(),
  faceapi.detectSingleFace(await canvas.loadImage('b.jpg')).withFaceLandmarks().withFaceDescriptor(),
]);

if (a && b) {
  const d = faceapi.euclideanDistance(a.descriptor, b.descriptor);
  console.log('distance:', d, d < 0.6 ? '(same person)' : '(different)');
}
```

## Running the official examples

```bash
git clone https://github.com/justadudewhohacks/face-api.js.git

# browser
cd face-api.js/examples/examples-browser && npm i && npm start  # http://localhost:3000/

# node
cd face-api.js/examples/examples-nodejs && npm i
ts-node faceDetection.ts          # or: tsc faceDetection.ts && node faceDetection.js
```

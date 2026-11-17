# API Reference

Precise reference for face-api.js v0.22.2. All names verified against the published package source.

## Input types

`TNetInput` accepted by all detection functions:

- `HTMLImageElement` | `HTMLVideoElement` | `HTMLCanvasElement`
- the element's `id` as a string (e.g. `'myImg'`)
- `tf.Tensor3D` | `tf.Tensor4D` (Node.js / tensor input)

## Detection entry points

```ts
detectAllFaces(input, options? = new SsdMobilenetv1Options()): DetectAllFacesTask
detectSingleFace(input, options? = new SsdMobilenetv1Options()): DetectSingleFaceTask
```

Both return thenable, chainable task objects. Chain methods:

| Method | Adds to each result | Notes |
|--------|--------------------|-------|
| `.withFaceLandmarks(useTinyModel?)` | `landmarks`, `unshiftedLandmarks`, `alignedRect` | `useTinyModel=true` → 80 KB tiny model |
| `.withFaceDescriptor()` | `descriptor` (Float32Array, 128) | single-face task (singular) |
| `.withFaceDescriptors()` | `descriptor` (Float32Array, 128) | all-faces task (plural) |
| `.withFaceExpressions()` | `expressions` (`FaceExpressions`) | optionally preceded by `.withFaceLandmarks()` (alignment → more stable) |
| `.withAgeAndGender()` | `age` (number), `gender`, `genderProbability` | optionally preceded by `.withFaceLandmarks()` |

Skipping `.withFaceLandmarks()` before `.withFaceExpressions()` / `.withAgeAndGender()` is allowed but skips the face alignment step (less stable accuracy).

### Low-level direct forward API

Alternative to the high-level chained tasks — call each net directly (input is a **face image region**, not the full frame, for landmark/descriptor/expression/age steps):

```ts
faceapi.ssdMobilenetv1(input, options?)   // boxes
faceapi.tinyFaceDetector(input, options?)  // boxes
faceapi.tinyYolov2(input, options?)        // boxes
faceapi.mtcnn(input, options)              // boxes + 5-point landmarks
faceapi.detectFaceLandmarks(faceImage)     // 68 landmarks
faceapi.detectFaceLandmarksTiny(faceImage) // 68 landmarks (tiny model)
faceapi.computeFaceDescriptor(alignedFaceImage)  // 128-d descriptor
faceapi.recognizeFaceExpressions(faceImage)      // FaceExpressions
faceapi.predictAgeAndGender(faceImage)           // { age, gender, genderProbability }
// aliases: faceapi.locateFaces === faceapi.ssdMobilenetv1
//          faceapi.detectLandmarks === faceapi.detectFaceLandmarks
```

### Detector options

```ts
interface ISsdMobilenetv1Options {
  minConfidence?: number; // default 0.5
  maxResults?: number;    // default 100
}
// new faceapi.SsdMobilenetv1Options({ minConfidence: 0.8 })

interface ITinyFaceDetectorOptions {
  inputSize?: number;     // default 416; must be divisible by 32
                          // 128,160,224,320,416,512,608; smaller = faster,
                          // larger = better at small faces
  scoreThreshold?: number;// default 0.5
}
// new faceapi.TinyFaceDetectorOptions({ inputSize: 320 })

interface IMtcnnOptions {
  minFaceSize?: number;      // default 20; higher = faster, misses small faces
  scoreThresholds?: number[];// default [0.6, 0.7, 0.7] (stages 1/2/3)
  scaleFactor?: number;      // default 0.709 (stage-1 pyramid step)
  maxNumScales?: number;     // default 10
  scaleSteps?: number[];     // explicit override of scaleFactor+maxNumScales
}
// new faceapi.MtcnnOptions({ minFaceSize: 100, scaleFactor: 0.8 })
```

## Model loaders

```ts
// convenience (call net.load(url), environment-aware)
loadSsdMobilenetv1Model(url)  loadTinyFaceDetectorModel(url)  loadMtcnnModel(url)
loadTinyYolov2Model(url)      loadFaceLandmarkModel(url)      loadFaceLandmarkTinyModel(url)
loadFaceRecognitionModel(url) loadFaceExpressionModel(url)    loadAgeGenderModel(url)

// registry singletons (each with loadFromUri / loadFromDisk / loadFromWeightMap)
faceapi.nets.ssdMobilenetv1  faceapi.nets.tinyFaceDetector  faceapi.nets.tinyYolov2
faceapi.nets.mtcnn  faceapi.nets.faceLandmark68Net  faceapi.nets.faceLandmark68TinyNet
faceapi.nets.faceRecognitionNet  faceapi.nets.faceExpressionNet  faceapi.nets.ageGenderNet
```

## Core utility classes / interfaces

```ts
interface IBox { x: number; y: number; width: number; height: number }
class Box implements IBox            // .area(), .round(), ...
class Rect extends Box               // new faceapi.Rect(x, y, w, h)
class Point { x; y }                 // faceapi.Point
class Dimensions { width; height }

interface IFaceDetection { score: number; box: Box }
class FaceDetection implements IFaceDetection   // .detection.score, .detection.box

interface IFaceLandmarks { positions: Point[]; shift: Point }
class FaceLandmarks                 // .positions (Point[]), .shift, .getRefPointsForAlignment()
class FaceLandmarks5                // MTCNN's 5 points (no contour getters)
class FaceLandmarks68               // full 68 points

// FaceLandmarks68 contour getters (68-point models only)
landmarks.getJawOutline()     // Point[]
landmarks.getLeftEyeBrow()    landmarks.getRightEyeBrow()
landmarks.getNose()           landmarks.getMouth()
landmarks.getLeftEye()        landmarks.getRightEye()

class FaceMatch                 // { label, distance } + .toString()

type WithFaceDetection<TSource> = TSource & { detection: FaceDetection }
type WithFaceLandmarks<TSource>  = TSource & { unshiftedLandmarks, landmarks, alignedRect }
type WithFaceDescriptor<TSource> = TSource & { descriptor: Float32Array }
type WithFaceExpressions<TSource> = TSource & { expressions: FaceExpressions }
type WithAge<TSource> = TSource & { age: number }
type WithGender<TSource> = TSource & { gender, genderProbability: number }

enum Gender { FEMALE = 'female', MALE = 'male' }
```

### FaceExpressions

`FaceExpressions` is an object holding a probability per expression. Expression keys: `neutral, happy, sad, angry, fearful, disgusted, surprised`.

```ts
class FaceExpressions {
  neutral: number; happy: number; sad: number; angry: number;
  fearful: number; disgusted: number; surprised: number;
  asSortedArray(): FaceExpressionPrediction[]  // [{ expression, probability }, ...] desc
}
type FaceExpression = 'neutral'|'happy'|'sad'|'angry'|'fearful'|'disgusted'|'surprised'
type FaceExpressionPrediction = { expression: FaceExpression; probability: number }
```

## Face recognition

```ts
class LabeledFaceDescriptors {
  constructor(label: string, descriptors: Float32Array[])
}
class FaceMatcher {
  constructor(inputs, distanceThreshold = 0.6)  // LabeledFaceDescriptors[] | WithFaceDescriptor<any>[] | Float32Array[]
  findBestMatch(descriptor): FaceMatch          // { label, distance }
  labeledDescriptors: LabeledFaceDescriptors[]
}
// FaceMatch.toString() → "label (distance)"
```

Threshold guidance: `distance < 0.6` is the default match cutoff (lower = stricter). Raw compare via `euclideanDistance`.

## Drawing functions

Drawing helpers live under the `faceapi.draw` namespace. `matchDimensions` and `resizeResults` are top-level `faceapi.*` exports.

```ts
faceapi.matchDimensions(canvas, { width, height })   // set canvas width/height
faceapi.resizeResults(results, { width, height })    // rescale boxes/landmarks to display size

faceapi.draw.drawDetections(canvas, detections, options?)   // options: { withScore?, boxColor?, lineWidth?, textColor?, fontSize?, label? }
faceapi.draw.drawFaceLandmarks(canvas, faceLandmarks, options?) // options: { drawLines?, lineWidth?, pointSize?, color? }
faceapi.draw.drawFaceExpressions(canvas, faceExpressions, minProbability = 0.05) // probability bars (only shows expressions ≥ minProbability)
faceapi.draw.drawContour(ctx, points, isClosed = false)   // polyline through points

faceapi.draw.DrawBox(box, options)                       // drawable box; options: { boxColor?, lineWidth?, label?, drawLabelOptions? }
faceapi.draw.DrawTextField(texts, anchor, options?)      // labeled text; options: { anchorPosition?, backgroundColor?, fontColor?, fontSize?, fontStyle?, padding? }
faceapi.draw.AnchorPosition = { TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT }
faceapi.getContext2dOrThrow(canvas): CanvasRenderingContext2D
```

Labeled box shorthand: `new faceapi.LabeledBox(new faceapi.Rect(x, y, w, h), 'label')`.

## Utility functions (top-level)

```ts
resizeResults(results, { width, height })
euclideanDistance(a, b): number                // Float32Array | number[]
extractFaces(input, detections): Promise<HTMLCanvasElement[]>   // crop regions
extractFaceTensors(imageTensor, detections): Promise<tf.Tensor[]>
createCanvasFromMedia(media, dims?): HTMLCanvasElement
imageTensorToCanvas(imgTensor, canvas?): Promise<HTMLCanvasElement>
imageToSquare(input, inputSize, centerImage = false): HTMLCanvasElement
fetchImage(uri): Promise<HTMLImageElement>
fetchJson(uri): Promise<T>
fetchNetWeights(uri): Promise<Float32Array>
loadWeightMap(uri | undefined, defaultModelName): Promise<tf.NamedTensorMap>
bufferToImage(buf: Blob): Promise<HTMLImageElement>
getMediaDimensions(input): Dimensions
isBrowser(): boolean
isNodejs(): boolean
isMediaElement(input): boolean
isMediaLoaded(media): boolean
awaitMediaLoaded(media): Promise
iou(box1, box2, isIOU = true): number
nonMaxSuppression(boxes, scores, iouThreshold, isIOU = true): number[]
```

## Low-level model constructors / factories

```ts
new faceapi.SsdMobilenetv1()   new faceapi.TinyFaceDetector()   new faceapi.Mtcnn()
new faceapi.TinyYolov2()       new faceapi.FaceLandmark68Net()  new faceapi.FaceLandmark68TinyNet()
new faceapi.FaceRecognitionNet()  new faceapi.FaceExpressionNet()  new faceapi.AgeGenderNet()

createSsdMobilenetv1(weights)  createTinyFaceDetector(weights)  createMtcnn(weights)
createTinyYolov2(weights, withSeparableConvs = true)
createFaceDetectionNet(weights)   createFaceRecognitionNet(weights)
```

## Environment

```ts
faceapi.env.monkeyPatch({ Canvas, Image, ImageData })  // Node.js polyfills (from 'canvas')
faceapi.env                                            // isBrowser / isNodejs flags, etc.
```
# After Effects ExtendScript API Reference

## Core Objects

### app
The global application object.

```jsx
app.version;           // "22.0"
app.name;              // "Adobe After Effects 2022"
app.buildName;         // "After Effects"
app.buildNumber;       // "22.0.0"
```

### app.project
The current project.

```jsx
app.project.items;     // Project items (comps, folders, footage)
app.project.activeItem;// Currently selected item
app.project.renderQueue; // Render queue
```

### CompItem
A composition.

```jsx
var comp = app.project.items.addComp("MyComp", 1920, 1080, 1, 30, 300);
comp.width;            // 1920
comp.height;           // 1080
comp.pixelAspect;      // 1
comp.framerate;        // 30
comp.duration;         // 300 (frames)
comp.layers;           // Layer collection
```

### Layer
A layer in a composition.

```jsx
var layer = comp.layers.addSolid([1,0,0], "Red Solid", 1920, 1080, 1);
layer.name;            // "Red Solid"
layer.enabled;         // true/false
layer.startTime;       // Start time in seconds
layer.outPoint;        // End time in seconds
```

### Property
Animatable properties.

```jsx
layer.property("ADBE Transform Group");
layer.property("ADBE Position");
layer.property("ADBE Opacity");
layer.property("ADBE Effect Parade"); // Effects
```

---

## Common Property Names

| Property | Match Name |
|----------|------------|
| Position | "ADBE Position" |
| Scale | "ADBE Scale" |
| Rotation | "ADBE Rotate" |
| Opacity | "ADBE Opacity" |
| Anchor Point | "ADBE Anchor Point" |
| Effects | "ADBE Effect Parade" |

---

## Keyframe Operations

```jsx
// Add keyframe
var posProp = layer.property("ADBE Position");
posProp.setValueAtTime(0, [960, 540]);
posProp.setValueAtTime(2, [1200, 540]);

// Get keyframes
var numKeys = posProp.numKeys;
var keyTime = posProp.keyTime(1);
var keyValue = posProp.keyValue(1);
```

---

## Effect Operations

```jsx
// Add effect
var effectProp = layer.property("ADBE Effect Parade");
var blur = effectProp.addProperty("ADBE Gaussian Blur");
blur.property("ADBE Gaussian Blur 0").setValue(50);

// Get effect by name
var effect = layer.property("ADBE Effect Parade").property("Gaussian Blur");
```

---

## File Operations

```jsx
// Import file
var file = new File("./myimage.png");
var footage = app.project.importFileWithSequence(file, false);

// Save project
app.project.save();
app.project.saveWithDialog();

// Close project
app.project.close();
```

---

## Render Queue

```jsx
// Add to render queue
var comp = app.project.activeItem;
var RQ = app.project.renderQueue;
var item = RQ.items.add(comp);

// Configure output
var output = item.outputs[1];
output.file = new File("./output.mov");

// Render
RQ.render();
```

// After Effects ExtendScript - Create Composition
// Usage: File > Scripts > Run Script File

function createComposition(name, width, height, duration, framerate) {
    var comp = app.project.items.addComp(
        name,
        width,
        height,
        1,          // pixel aspect
        framerate,
        duration    // in frames
    );
    
    return comp;
}

// Example: Create 1920x1080, 30fps, 10 second comp
var myComp = createComposition("MyComp", 1920, 1080, 300, 30);

// Add a solid layer
var solid = myComp.layers.addSolid(
    [1, 0, 0],      // RGB color (red)
    "Red Solid",
    1920,
    1080,
    1               // pixel aspect
);

// Position at center
solid.property("ADBE Position").setValue([960, 540]);

// Add scale keyframes
var scaleProp = solid.property("ADBE Scale");
scaleProp.setValueAtTime(0, [0, 0]);
scaleProp.setValueAtTime(2, [100, 100]);

// Add Gaussian Blur effect
var effectProp = solid.property("ADBE Effect Parade");
var blur = effectProp.addProperty("ADBE Gaussian Blur");
blur.property("ADBE Gaussian Blur 0").setValue(20);

// Log success
writeLn("Composition created: " + myComp.name);

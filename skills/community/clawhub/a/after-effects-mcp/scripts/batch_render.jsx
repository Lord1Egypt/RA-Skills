// After Effects ExtendScript - Batch Render
// Usage: Queue multiple compositions for rendering

function batchRender(compsArray, outputPath) {
    var RQ = app.project.renderQueue;
    
    for (var i = 0; i < compsArray.length; i++) {
        var compName = compsArray[i];
        var comp = app.project.itemByName(compName);
        
        if (comp && comp instanceof CompItem) {
            var rqItem = RQ.items.add(comp);
            
            // Configure output module
            var output = rqItem.outputs[1];
            output.file = new File(outputPath + "/" + compName + ".mov");
            
            // Set render settings
            rqItem.timeSpanStart = 0;
            rqItem.timeSpanDuration = comp.duration;
            
            writeLn("Added to queue: " + compName);
        } else {
            writeLn("Composition not found: " + compName);
        }
    }
    
    writeLn("Total items in queue: " + RQ.items.length);
}

// Example usage:
// batchRender(["Comp1", "Comp2", "Comp3"], "./renders");

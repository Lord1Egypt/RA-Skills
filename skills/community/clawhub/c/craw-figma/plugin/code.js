/// Craw Figma Connector — Plugin Code (ES5)
/// HTTP polling architecture: plugin polls commands via UI proxy, executes them

var POLL_INTERVAL = 1500;
var pollTimer = null;
var selectionTimer = null;

function postUI(type, data) {
  var msg = {};
  msg.type = type;
  if (data) {
    var keys = Object.keys(data);
    for (var i = 0; i < keys.length; i++) {
      msg[keys[i]] = data[keys[i]];
    }
  }
  figma.ui.postMessage(msg);
}

function hasFills(node) { return "fills" in node; }
function hasResize(node) { return "resize" in node; }
function hasPosition(node) { return "x" in node && "y" in node; }
function hasStrokes(node) { return "strokes" in node; }
function hasEffects(node) { return "effects" in node; }
function hasCornerRadius(node) { return "cornerRadius" in node; }

// Helper: converts legacy fillColor + opacity to the fills[] format expected by the plugin
// Supports both formats: fills[] or fillColor{r,g,b} + opacity
function resolveFills(p) {
  if (p.fills) return p.fills;
  if (p.fillColor) {
    var fill = { type: "SOLID", color: p.fillColor };
    if (typeof p.opacity !== "undefined") fill.opacity = p.opacity;
    return [fill];
  }
  return null;
}
// Helper: converts legacy strokeColor to strokes[]
function resolveStrokes(p) {
  if (p.strokes) return p.strokes;
  if (p.strokeColor) {
    var stroke = { type: "SOLID", color: p.strokeColor };
    if (typeof p.opacity !== "undefined") stroke.opacity = p.opacity;
    return [stroke];
  }
  return null;
}

var commands = {};

// ── PRIMITIVE SHAPES ──

commands.createRectangle = function(p) {
  var rect = figma.createRectangle();
  rect.x = typeof p.x !== "undefined" ? p.x : 0;
  rect.y = typeof p.y !== "undefined" ? p.y : 0;
  rect.resize(typeof p.width !== "undefined" ? p.width : 200, typeof p.height !== "undefined" ? p.height : 100);
  if (p.cornerRadius && hasCornerRadius(rect)) rect.cornerRadius = p.cornerRadius;
  var _fills = resolveFills(p);
  if (_fills && hasFills(rect)) rect.fills = _fills;
  if (p.strokes && hasStrokes(rect)) rect.strokes = p.strokes;
  if (p.strokeWeight) rect.strokeWeight = p.strokeWeight;
  if (p.effects && hasEffects(rect)) rect.effects = p.effects;
  if (p.name) rect.name = p.name;
  figma.currentPage.appendChild(rect);
  var result = {};
  result.id = rect.id; result.name = rect.name;
  result.x = rect.x; result.y = rect.y;
  result.width = rect.width; result.height = rect.height;
  return result;
};

commands.createFrame = function(p) {
  var frame = figma.createFrame();
  frame.x = typeof p.x !== "undefined" ? p.x : 0;
  frame.y = typeof p.y !== "undefined" ? p.y : 0;
  frame.resize(typeof p.width !== "undefined" ? p.width : 400, typeof p.height !== "undefined" ? p.height : 300);
  var _fills = resolveFills(p);
  if (_fills && hasFills(frame)) frame.fills = _fills;
  if (p.strokes && hasStrokes(frame)) frame.strokes = p.strokes;
  if (p.strokeWeight) frame.strokeWeight = p.strokeWeight;
  if (p.effects && hasEffects(frame)) frame.effects = p.effects;
  if (p.cornerRadius && hasCornerRadius(frame)) frame.cornerRadius = p.cornerRadius;
  if (p.name) frame.name = p.name;
  // Auto layout — direct properties (from auto_layout.js and shape_generator.js)
  if (p.layoutMode) {
    frame.layoutMode = p.layoutMode;
    if (p.primaryAxisSizingMode) frame.primaryAxisSizingMode = p.primaryAxisSizingMode;
    if (p.counterAxisSizingMode) frame.counterAxisSizingMode = p.counterAxisSizingMode;
    if (typeof p.paddingLeft !== "undefined") frame.paddingLeft = p.paddingLeft;
    if (typeof p.paddingRight !== "undefined") frame.paddingRight = p.paddingRight;
    if (typeof p.paddingTop !== "undefined") frame.paddingTop = p.paddingTop;
    if (typeof p.paddingBottom !== "undefined") frame.paddingBottom = p.paddingBottom;
    if (typeof p.itemSpacing !== "undefined") frame.itemSpacing = p.itemSpacing;
    if (p.primaryAxisAlignItems) frame.primaryAxisAlignItems = p.primaryAxisAlignItems;
    if (p.counterAxisAlignItems) frame.counterAxisAlignItems = p.counterAxisAlignItems;
  }
  // Legacy autoLayout support
  if (!p.layoutMode && p.autoLayout) {
    frame.layoutMode = p.autoLayout.mode || "NONE";
    if (p.autoLayout.padding) { frame.paddingLeft = p.autoLayout.padding; frame.paddingRight = p.autoLayout.padding; frame.paddingTop = p.autoLayout.padding; frame.paddingBottom = p.autoLayout.padding; }
    if (p.autoLayout.itemSpacing) frame.itemSpacing = p.autoLayout.itemSpacing;
    if (p.autoLayout.primaryAxisAlignItems) frame.primaryAxisAlignItems = p.autoLayout.primaryAxisAlignItems;
    if (p.autoLayout.counterAxisAlignItems) frame.counterAxisAlignItems = p.autoLayout.counterAxisAlignItems;
  }
  figma.currentPage.appendChild(frame);
  var result = {};
  result.id = frame.id; result.name = frame.name;
  return result;
};

commands.createEllipse = function(p) {
  var ell = figma.createEllipse();
  ell.x = typeof p.x !== "undefined" ? p.x : 0;
  ell.y = typeof p.y !== "undefined" ? p.y : 0;
  ell.resize(typeof p.width !== "undefined" ? p.width : 100, typeof p.height !== "undefined" ? p.height : 100);
  var _fills = resolveFills(p);
  if (_fills && hasFills(ell)) ell.fills = _fills;
  if (p.strokes && hasStrokes(ell)) ell.strokes = p.strokes;
  if (p.strokeWeight) ell.strokeWeight = p.strokeWeight;
  if (p.effects && hasEffects(ell)) ell.effects = p.effects;
  if (p.name) ell.name = p.name;
  // Arc slicing
  if (typeof p.startAngle !== "undefined") ell.arcData = { startingAngle: p.startAngle, endingAngle: p.endingAngle || 0, innerRadius: p.innerRadius || 0 };
  figma.currentPage.appendChild(ell);
  var result = {};
  result.id = ell.id; result.name = ell.name;
  return result;
};

commands.createPolygon = function(p) {
  var poly = figma.createPolygon();
  poly.x = typeof p.x !== "undefined" ? p.x : 0;
  poly.y = typeof p.y !== "undefined" ? p.y : 0;
  poly.resize(typeof p.width !== "undefined" ? p.width : 100, typeof p.height !== "undefined" ? p.height : 100);
  poly.pointCount = typeof p.pointCount !== "undefined" ? p.pointCount : 3;
  var _fills = resolveFills(p);
  if (_fills && hasFills(poly)) poly.fills = _fills;
  if (p.strokes && hasStrokes(poly)) poly.strokes = p.strokes;
  if (p.strokeWeight) poly.strokeWeight = p.strokeWeight;
  if (p.effects && hasEffects(poly)) poly.effects = p.effects;
  if (p.name) poly.name = p.name;
  figma.currentPage.appendChild(poly);
  var result = {};
  result.id = poly.id; result.name = poly.name; result.pointCount = poly.pointCount;
  return result;
};

commands.createStar = function(p) {
  var star = figma.createStar();
  star.x = typeof p.x !== "undefined" ? p.x : 0;
  star.y = typeof p.y !== "undefined" ? p.y : 0;
  star.resize(typeof p.width !== "undefined" ? p.width : 100, typeof p.height !== "undefined" ? p.height : 100);
  star.pointCount = typeof p.pointCount !== "undefined" ? p.pointCount : 5;
  star.innerRadius = typeof p.innerRadius !== "undefined" ? p.innerRadius : 0.5;
  var _fills = resolveFills(p);
  if (_fills && hasFills(star)) star.fills = _fills;
  if (p.strokes && hasStrokes(star)) star.strokes = p.strokes;
  if (p.strokeWeight) star.strokeWeight = p.strokeWeight;
  if (p.effects && hasEffects(star)) star.effects = p.effects;
  if (p.name) star.name = p.name;
  figma.currentPage.appendChild(star);
  var result = {};
  result.id = star.id; result.name = star.name; result.pointCount = star.pointCount;
  return result;
};

commands.createLine = function(p) {
  var line = figma.createLine();
  line.x = typeof p.x !== "undefined" ? p.x : 0;
  line.y = typeof p.y !== "undefined" ? p.y : 0;
  line.resize(typeof p.width !== "undefined" ? p.width : 200, typeof p.height !== "undefined" ? p.height : 0);
  if (p.strokes && hasStrokes(line)) line.strokes = p.strokes;
  if (p.strokeWeight) line.strokeWeight = p.strokeWeight;
  if (p.name) line.name = p.name;
  figma.currentPage.appendChild(line);
  var result = {};
  result.id = line.id; result.name = line.name;
  return result;
};

// Alias: createVectorNetwork calls createVector under the hood
commands.createVectorNetwork = function(p) {
  return commands.createVector(p);
};

commands.createVector = function(p) {
  // p.vertices = array of {x, y}
  // p.segments = array of {start, end, tangentStart?, tangentEnd?}
  // Each vertex: { x, y, strokeCap?, cornerRadius? }
  // Each segment: { start, end, tangentStart?:{x,y}, tangentEnd?:{x,y} }
  var vector = figma.createVector();
  vector.x = typeof p.x !== "undefined" ? p.x : 0;
  vector.y = typeof p.y !== "undefined" ? p.y : 0;
  var _fills = resolveFills(p);
  if (_fills && hasFills(vector)) vector.fills = _fills;
  if (p.strokes && hasStrokes(vector)) vector.strokes = p.strokes;
  if (p.strokeWeight) vector.strokeWeight = p.strokeWeight;
  if (p.effects && hasEffects(vector)) vector.effects = p.effects;
  if (p.name) vector.name = p.name;
  // Build vector network — no regions, let Figma auto-close if p.closed
  if (p.vertices && p.segments) {
    var vtx = [];
    for (var i = 0; i < p.vertices.length; i++) {
      var v = p.vertices[i];
      vtx.push({ x: v.x, y: v.y, strokeCap: v.strokeCap || "NONE", cornerRadius: v.cornerRadius || 0 });
    }
    var segs = [];
    for (var j = 0; j < p.segments.length; j++) {
      var s = p.segments[j];
      var seg = { start: s.start, end: s.end };
      if (s.tangentStart) seg.tangentStart = s.tangentStart;
      if (s.tangentEnd) seg.tangentEnd = s.tangentEnd;
      segs.push(seg);
    }
    // Build network without regions (regions is read-only after assignment)
    var network = { vertices: vtx, segments: segs };
    if (p.closed) {
      // Build regions array before assigning
      var regionLoops = [];
      var loop = [];
      for (var k = 0; k < segs.length; k++) {
        loop.push(k);
      }
      regionLoops.push({ windingRule: "EVENODD", loops: [loop] });
      network.regions = regionLoops;
    }
    vector.vectorNetwork = network;
  }
  figma.currentPage.appendChild(vector);
  var result = {};
  result.id = vector.id; result.name = vector.name;
  return result;
};

// ── FONT LOADING ──
// Pre-load common fonts at plugin start so createText works without errors
var loadedFonts = {};

function addLoadedFont(name, style) {
  var key = name + '_' + (style || 'Regular');
  loadedFonts[key] = true;
}

function loadDefaultFonts() {
  var fontPairs = [
    { family: 'Inter', style: 'Regular' },
    { family: 'Inter', style: 'Medium' },
    { family: 'Inter', style: 'Bold' },
    { family: 'Inter', style: 'Semi Bold' },
    { family: 'Inter', style: 'Light' },
    { family: 'Roboto', style: 'Regular' },
    { family: 'Roboto', style: 'Medium' },
    { family: 'JetBrains Mono', style: 'Regular' },
    { family: 'JetBrains Mono', style: 'Bold' },
    // DR's Lab custom fonts — exact Figma dropdown names (verified manually)
    { family: 'Inter', style: 'Regular' },
    { family: 'Saint', style: 'Regular' },
    { family: 'FREE FAT FONT', style: 'Regular' },
  ];
  var promises = [];
  for (var i = 0; i < fontPairs.length; i++) {
    (function(fp) {
      promises.push(
        figma.loadFontAsync(fp).then(function() {
          addLoadedFont(fp.family, fp.style);
        }).catch(function() {})
      );
    })(fontPairs[i]);
  }
  return Promise.all(promises);
}

commands.createText = function(p) {
  var text = figma.createText();
  text.characters = typeof p.characters !== "undefined" ? p.characters : "Text";
  text.x = typeof p.x !== "undefined" ? p.x : 0;
  text.y = typeof p.y !== "undefined" ? p.y : 0;
  
  // If fontFamily specified, try to load it
  var fontFamily = (p.fontName && p.fontName.family) || 'Inter';
  var fontStyle = (p.fontName && p.fontName.style) || 'Regular';
  var loadKey = fontFamily + '_' + fontStyle;
  
  if (!loadedFonts[loadKey]) {
    // Font not preloaded — try loading synchronously
    throw new Error('Font "' + fontFamily + ' ' + fontStyle + '" not loaded. Preload with figma.loadFontAsync().');
  }
  
  if (p.name) text.name = p.name;
  if (p.fontSize) text.fontSize = p.fontSize;
  var _fills = resolveFills(p);
  if (_fills && hasFills(text)) text.fills = _fills;
  if (p.textAlignHorizontal) text.textAlignHorizontal = p.textAlignHorizontal;
  if (p.fontName) text.fontName = p.fontName;
  if (p.letterSpacing) {
    if (typeof p.letterSpacing === 'number') { text.letterSpacing = { value: p.letterSpacing, unit: 'PIXELS' }; }
    else if (p.letterSpacing.value !== undefined) { text.letterSpacing = p.letterSpacing; }
  }
  if (p.lineHeight) text.lineHeight = p.lineHeight;
  if (p.textAutoResize) text.textAutoResize = p.textAutoResize;
  figma.currentPage.appendChild(text);
  var result = {};
  result.id = text.id; result.name = text.name;
  return result;
};

// ── STYLING ──

commands.setFillColor = function(p) {
  var node = figma.getNodeById(p.id);
  if (!node || !hasFills(node)) throw new Error("Node not found or no fills");
  node.fills = [{ type: "SOLID", color: p.color, opacity: p.opacity || 1 }];
  var result = {};
  result.id = node.id; result.fillSet = true;
  return result;
};

commands.setGradient = function(p) {
  var node = figma.getNodeById(p.id);
  if (!node || !hasFills(node)) throw new Error("Node not found or no fills");
  var gradType = p.gradientType || "LINEAR";
  var stops = p.stops || [];
  // Build gradient transform
  var transform = [[1, 0, 0], [0, 1, 0]];
  if (p.transform) transform = p.transform;
  if (stops.length === 0) {
    stops = [{ position: 0, color: { r: 0, g: 0, b: 0, a: 1 } }, { position: 1, color: { r: 1, g: 1, b: 1, a: 1 } }];
  }
  node.fills = [{
    type: "GRADIENT_" + gradType,
    gradientStops: stops,
    gradientTransform: transform,
    opacity: p.opacity || 1
  }];
  var result = {};
  result.id = node.id; result.gradientSet = true;
  return result;
};

commands.setStroke = function(p) {
  var node = figma.getNodeById(p.id);
  if (!node) throw new Error("Node not found");
  if (p.color) node.strokes = [{ type: "SOLID", color: p.color, opacity: p.opacity || 1 }];
  if (typeof p.strokeWeight !== "undefined") node.strokeWeight = p.strokeWeight;
  if (p.strokeAlign) node.strokeAlign = p.strokeAlign;
  if (p.strokeCap) node.strokeCap = p.strokeCap;
  if (p.strokeJoin) node.strokeJoin = p.strokeJoin;
  if (p.dashPattern) node.dashPattern = p.dashPattern;
  var result = {};
  result.id = node.id; result.strokeSet = true;
  return result;
};

commands.setEffects = function(p) {
  var node = figma.getNodeById(p.id);
  if (!node || !hasEffects(node)) throw new Error("Node not found or no effects");
  node.effects = p.effects || [];
  var result = {};
  result.id = node.id; result.effectsSet = true;
  return result;
};

// ── NODE MANIPULATION ──

commands.selectNode = function(p) {
  if (p.id) {
    var node = figma.getNodeById(p.id);
    if (node) {
      if (p.addToSelection && figma.currentPage.selection.length > 0) {
        var sel = figma.currentPage.selection.slice(0);
        sel.push(node);
        figma.currentPage.selection = sel;
      } else {
        figma.currentPage.selection = [node];
      }
      figma.viewport.scrollAndZoomIntoView([node]);
      var result = {};
      result.found = true;
      return result;
    }
  }
  var result = {};
  result.found = false;
  return result;
};

commands.updateNode = function(p) {
  var node = figma.getNodeById(p.id);
  if (!node) throw new Error("Node not found: " + p.id);
  if (typeof p.x !== "undefined" && hasPosition(node)) node.x = p.x;
  if (typeof p.y !== "undefined" && hasPosition(node)) node.y = p.y;
  if (p.resize && hasResize(node)) node.resize(p.resize.width, p.resize.height);
  var _fills = resolveFills(p);
  if (_fills && hasFills(node)) node.fills = _fills;
  if (p.effects && hasEffects(node)) node.effects = p.effects;
  if (p.strokes && hasStrokes(node)) node.strokes = p.strokes;
  if (typeof p.strokeWeight !== "undefined") node.strokeWeight = p.strokeWeight;
  if (p.cornerRadius && hasCornerRadius(node)) node.cornerRadius = p.cornerRadius;
  if (p.opacity && "opacity" in node) node.opacity = p.opacity;
  if (p.locked && "locked" in node) node.locked = p.locked;
  if (p.visible !== undefined && "visible" in node) node.visible = p.visible;
  if (p.name) node.name = p.name;
  // Auto layout properties for updateNode (used by auto_layout.js applyAutoLayout)
  if (p.layoutMode) node.layoutMode = p.layoutMode;
  if (p.primaryAxisSizingMode) node.primaryAxisSizingMode = p.primaryAxisSizingMode;
  if (p.counterAxisSizingMode) node.counterAxisSizingMode = p.counterAxisSizingMode;
  if (typeof p.paddingLeft !== "undefined") node.paddingLeft = p.paddingLeft;
  if (typeof p.paddingRight !== "undefined") node.paddingRight = p.paddingRight;
  if (typeof p.paddingTop !== "undefined") node.paddingTop = p.paddingTop;
  if (typeof p.paddingBottom !== "undefined") node.paddingBottom = p.paddingBottom;
  if (typeof p.itemSpacing !== "undefined") node.itemSpacing = p.itemSpacing;
  if (p.primaryAxisAlignItems) node.primaryAxisAlignItems = p.primaryAxisAlignItems;
  if (p.counterAxisAlignItems) node.counterAxisAlignItems = p.counterAxisAlignItems;
  var result = {};
  result.id = node.id; result.name = node.name; result.updated = true;
  return result;
};

commands.deleteNode = function(p) {
  var result = {};
  if (p.id) {
    var node = figma.getNodeById(p.id);
    if (node) {
      node.remove();
      result.deleted = true;
      result.id = p.id;
      return result;
    }
  }
  result.deleted = false;
  return result;
};

commands.getSelection = function() {
  return figma.currentPage.selection.map(function(n) {
    var r = {};
    r.id = n.id; r.name = n.name; r.type = n.type; r.x = n.x; r.y = n.y; r.width = n.width; r.height = n.height;
    r.opacity = n.opacity || 1;
    r.visible = n.visible !== false;
    if (n.fills) r.fillCount = n.fills.length;
    return r;
  });
};

commands.getPageInfo = function() {
  var result = {};
  result.name = figma.currentPage.name;
  result.id = figma.currentPage.id;
  result.childCount = figma.currentPage.children.length;
  return result;
};

commands.groupSelection = function() {
  var sel = figma.currentPage.selection;
  if (sel.length < 2) throw new Error("Select at least 2 nodes");
  var group = figma.group(sel, figma.currentPage);
  var result = {};
  result.id = group.id; result.name = group.name;
  return result;
};

// ── BOOLEAN OPERATIONS ──

commands.booleanOperation = function(p) {
  var nodes = [];
  
  // Support both single node (union children) and nodeIds array (union separate nodes)
  if (p.nodeIds && p.nodeIds.length >= 2) {
    for (var i = 0; i < p.nodeIds.length; i++) {
      var n = figma.getNodeById(p.nodeIds[i]);
      if (n) nodes.push(n);
    }
  } else if (p.id) {
    var node = figma.getNodeById(p.id);
    if (!node) throw new Error("Node not found: " + p.id);
    if (node.children && node.children.length >= 2) {
      for (var i = 0; i < node.children.length; i++) {
        nodes.push(node.children[i]);
      }
    }
  }
  
  if (nodes.length < 2) throw new Error("Need at least 2 nodes for boolean operation");
  
  var parent = nodes[0].parent || figma.currentPage;
  var boolGroup = figma.union(nodes, parent);
  
  var op = p.operation || "UNION";
  switch (op.toUpperCase()) {
    case "SUBTRACT": boolGroup.booleanOperation = "SUBTRACT"; break;
    case "INTERSECT": boolGroup.booleanOperation = "INTERSECT"; break;
    case "EXCLUDE": boolGroup.booleanOperation = "EXCLUDE"; break;
    case "UNION": default: boolGroup.booleanOperation = "UNION"; break;
  }
  
  if (p.name) boolGroup.name = p.name;
  var _fills = resolveFills(p);
  if (_fills && hasFills(boolGroup)) boolGroup.fills = _fills;
  
  var result = {};
  result.id = boolGroup.id; result.name = boolGroup.name;
  result.booleanOperation = boolGroup.booleanOperation;
  return result;
};

commands.flatten = function(p) {
  var sel = figma.currentPage.selection;
  if (sel.length < 2) throw new Error("Select at least 2 nodes");
  var flattened = figma.flatten(sel, figma.currentPage);
  if (p.name) flattened.name = p.name;
  var result = {};
  result.id = flattened.id; result.name = flattened.name;
  return result;
};

// ── COMPONENTS ──

commands.createComponent = function(p) {
  if (p.fromFrameId) {
    var node = figma.getNodeById(p.fromFrameId);
    if (!node) throw new Error("Node not found: " + p.fromFrameId);
    var comp = figma.createComponentFromNode(node);
    if (p.name) comp.name = p.name;
    var result = {};
    result.id = comp.id; result.name = comp.name; result.type = "COMPONENT";
    return result;
  }
  var comp = figma.createComponent();
  comp.x = typeof p.x !== "undefined" ? p.x : 0;
  comp.y = typeof p.y !== "undefined" ? p.y : 0;
  comp.resize(typeof p.width !== "undefined" ? p.width : 200, typeof p.height !== "undefined" ? p.height : 200);
  var _fills = resolveFills(p);
  if (_fills && hasFills(comp)) comp.fills = _fills;
  if (p.effects && hasEffects(comp)) comp.effects = p.effects;
  if (p.name) comp.name = p.name;
  figma.currentPage.appendChild(comp);
  var result = {};
  result.id = comp.id; result.name = comp.name; result.type = "COMPONENT";
  return result;
};

commands.createInstance = function(p) {
  if (!p.componentId) throw new Error("componentId required");
  var compNode = figma.getNodeById(p.componentId);
  if (!compNode || compNode.type !== "COMPONENT") throw new Error("Component not found");
  var inst = compNode.createInstance();
  if (typeof p.x !== "undefined" && hasPosition(inst)) inst.x = p.x;
  if (typeof p.y !== "undefined" && hasPosition(inst)) inst.y = p.y;
  if (p.name) inst.name = p.name;
  figma.currentPage.appendChild(inst);
  var result = {};
  result.id = inst.id; result.name = inst.name; result.type = "INSTANCE";
  return result;
};

// ── LAYOUT HELPERS ──

commands.addAutoLayout = function(p) {
  var node = figma.getNodeById(p.id);
  if (!node) throw new Error("Node not found");
  if (!("layoutMode" in node)) throw new Error("Node does not support auto layout");
  node.layoutMode = p.mode || "NONE";
  if (typeof p.padding !== "undefined") { node.paddingLeft = p.padding; node.paddingRight = p.padding; node.paddingTop = p.padding; node.paddingBottom = p.padding; }
  if (typeof p.paddingTop !== "undefined") node.paddingTop = p.paddingTop;
  if (typeof p.paddingBottom !== "undefined") node.paddingBottom = p.paddingBottom;
  if (typeof p.paddingLeft !== "undefined") node.paddingLeft = p.paddingLeft;
  if (typeof p.paddingRight !== "undefined") node.paddingRight = p.paddingRight;
  if (typeof p.itemSpacing !== "undefined") node.itemSpacing = p.itemSpacing;
  if (p.primaryAxisAlignItems) node.primaryAxisAlignItems = p.primaryAxisAlignItems;
  if (p.counterAxisAlignItems) node.counterAxisAlignItems = p.counterAxisAlignItems;
  if (typeof p.counterAxisSizingMode !== "undefined") node.counterAxisSizingMode = p.counterAxisSizingMode;
  if (typeof p.primaryAxisSizingMode !== "undefined") node.primaryAxisSizingMode = p.primaryAxisSizingMode;
  if (typeof p.strokeWeight !== "undefined") node.strokeWeight = p.strokeWeight;
  if (typeof p.itemReverseZIndex !== "undefined") node.itemReverseZIndex = p.itemReverseZIndex;
  if (typeof p.strokesIncludedInLayout !== "undefined") node.strokesIncludedInLayout = p.strokesIncludedInLayout;
  var result = {};
  result.id = node.id; result.layoutMode = node.layoutMode;
  return result;
};

commands.constrainProportions = function(p) {
  var node = figma.getNodeById(p.id);
  if (!node) throw new Error("Node not found");
  if ("constrainProportions" in node) node.constrainProportions = p.value !== false;
  var result = {};
  result.id = node.id; result.constrainProportions = node.constrainProportions || false;
  return result;
};

// ── EXPORT ──

commands.exportNode = function(p) {
  var node = figma.getNodeById(p.id);
  if (!node) throw new Error("Node not found: " + p.id);
  var settings = { format: p.format || "PNG", constraint: { type: "SCALE", value: p.scale || 1 } };
  if (p.contentsOnly !== undefined) settings.contentsOnly = p.contentsOnly;
  if (p.asBase64) {
    return node.exportAsync(settings).then(function(bytes) {
      var b64 = figma.base64Encode(bytes);
      postUI("export-base64", { commandId: "export-" + p.id, id: p.id, base64: b64, format: settings.format, name: node.name });
      return { exported: true, format: settings.format, size: bytes.length, base64Sent: true };
    });
  }
  var bytes = node.exportAsync(settings);
  var result = {};
  result.exported = true; result.format = settings.format; result.size = bytes.length;
  return result;
};

// ── HELPERS ──

commands.duplicateNode = function(p) {
  var node = figma.getNodeById(p.id);
  if (!node) throw new Error("Node not found: " + p.id);
  var clone = node.clone();
  if (hasPosition(clone)) { clone.x = (clone.x || 0) + (p.offsetX || 100); clone.y = (clone.y || 0) + (p.offsetY || 100); }
  figma.currentPage.appendChild(clone);
  var result = {};
  result.id = clone.id; result.name = clone.name;
  return result;
};

commands.moveNodes = function(p) {
  var node = figma.getNodeById(p.id);
  if (!node) throw new Error("Node not found: " + p.id);
  if (p.parentId) {
    var parent = figma.getNodeById(p.parentId);
    if (!parent || !(parent.type === "FRAME" || parent.type === "GROUP" || parent.type === "COMPONENT")) throw new Error("Invalid parent");
    parent.appendChild(node);
  }
  var result = {};
  result.id = node.id;
  if (parent) result.parentId = p.parentId;
  return result;
};

// ── SVG IMPORT ──
// Uses Figma's native SVG parser for perfect vector shapes

commands.importSvg = function(p) {
  if (!p.svg) throw new Error("Missing 'svg' parameter");
  
  // figma.createNodeFromSvgAsync is a standard Figma API method
  var promise = figma.createNodeFromSvgAsync(p.svg);
  
  return promise.then(function(nodes) {
    var mainNode = null;
    var nodeIds = [];
    
    for (var i = 0; i < nodes.length; i++) {
      var n = nodes[i];
      figma.currentPage.appendChild(n);
      nodeIds.push(n.id);
      if (i === 0) mainNode = n;
    }
    
    // If we got multiple nodes, group them
    if (nodes.length > 1) {
      figma.currentPage.selection = nodes;
      var group = figma.group(nodes, figma.currentPage);
      mainNode = group;
    }
    
    var result = {};
    result.id = mainNode.id;
    result.name = mainNode.name;
    result.nodeCount = nodes.length;
    result.nodeIds = nodeIds;
    
    return result;
  });
};

// ── COMMAND EXECUTION ──

function executeCommand(cmd) {
  var command = cmd.command;
  var payload = cmd.payload || {};
  var id = cmd.id;

  var logMsg = {};
  logMsg.text = "Exec: " + command;
  logMsg.level = "cmd";
  postUI("log", logMsg);

  var handler = commands[command];
  if (!handler) {
    var errMsg = {};
    errMsg.text = "Unknown: " + command;
    errMsg.level = "err";
    postUI("log", errMsg);
    sendResult(id, "error", { error: "Unknown command: " + command });
    return;
  }

  try {
    var result = handler(payload);
    if (result && typeof result.then === "function") {
      result.then(
        function(res) {
          var doneMsg = {};
          doneMsg.text = "Done";
          doneMsg.level = "done";
          postUI("log", doneMsg);
          sendResult(id, "ok", res);
        },
        function(err) {
          var errMsg = {};
          errMsg.text = "Error: " + (err.message || String(err));
          errMsg.level = "err";
          postUI("log", errMsg);
          sendResult(id, "error", { error: err.message || String(err) });
        }
      );
    } else {
      var doneMsg = {};
      doneMsg.text = "Done";
      doneMsg.level = "done";
      postUI("log", doneMsg);
      sendResult(id, "ok", result);
    }
  } catch(err) {
    var errMsg = {};
    errMsg.text = "Error: " + (err.message || String(err));
    errMsg.level = "err";
    postUI("log", errMsg);
    sendResult(id, "error", { error: err.message || String(err) });
  }
}

function sendResult(id, status, data) {
  postUI("command-result", { commandId: id, status: status, data: data });
}

function startPolling() {
  function poll() { postUI("poll-command", {}); }
  pollTimer = setInterval(poll, POLL_INTERVAL);
  setTimeout(poll, 300);
}

function startSelectionUpdates() {
  selectionTimer = setInterval(function() {
    try {
      var pageMsg = {};
      pageMsg.name = figma.currentPage.name;
      pageMsg.id = figma.currentPage.id;
      pageMsg.childCount = figma.currentPage.children.length;
      postUI("page-info", pageMsg);

      var selArray = figma.currentPage.selection.map(function(n) {
        var r = {};
        r.id = n.id; r.name = n.name; r.type = n.type;
        r.x = n.x; r.y = n.y; r.width = n.width; r.height = n.height;
        return r;
      });
      var selMsg = {};
      selMsg.nodes = selArray;
      postUI("selection-update", selMsg);
    } catch(e) {}
  }, 1500);
}

figma.showUI(__html__, { width: 320, height: 400 });
figma.skipInvisibleInstanceChildren = true;

// Load fonts before starting operations
loadDefaultFonts().then(function() {
  var logMsg = {};
  logMsg.text = "Plugin loaded (fonts ready)";
  logMsg.level = "";
  postUI("log", logMsg);
  startPolling();
  startSelectionUpdates();
}).catch(function(err) {
  // Even if some fonts fail, start anyway
  var logMsg = {};
  logMsg.text = "Plugin loaded (fonts partial)";
  logMsg.level = "";
  postUI("log", logMsg);
  startPolling();
  startSelectionUpdates();
});

figma.ui.onmessage = function(msg) {
  if (msg.type === "command") {
    executeCommand(msg.cmd);
    return;
  }
};

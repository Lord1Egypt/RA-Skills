#!/usr/bin/env node
/**
 * Shape Generator — General-purpose Figma shape creation
 *
 * Supports: rectangles, ellipses, regular polygons, stars, arbitrary paths,
 * hearts, and compound shapes (union, subtract, intersect, exclude).
 *
 * Smart positioning: 3-column grid starting from (100,100), padding 40.
 * DR's Lab style tokens: bg #0A0F18, accent #247DFF, text #E8EEF5.
 *
 * Usage:
 *   node shape_generator.js <command> [params]
 *
 * Commands:
 *   generate    — create a single shape
 *   grid        — create a grid of shapes from a JSON file or inline array
 *   test-basic  — demo: rectangle, ellipse, polygon, star
 *   test-union  — demo: union of two circles
 */

var http = require('http');
var CONNECTOR = process.env.FIGMA_CONNECTOR || 'http://localhost:9199';

// ── Design Tokens (DR's Lab) ──
var COLORS = {
  bg:     { r: 0.04, g: 0.06, b: 0.09 },  // #0A0F18
  accent: { r: 0.14, g: 0.49, b: 1.00 },  // #247DFF
  text:   { r: 0.91, g: 0.93, b: 0.96 },  // #E8EEF5
  surface:{ r: 0.09, g: 0.13, b: 0.20 },  // #172233
  muted:  { r: 0.35, g: 0.39, b: 0.47 },  // #5A6478
  green:  { r: 0.20, g: 0.80, b: 0.40 },  // #33CC66
  red:    { r: 0.90, g: 0.20, b: 0.20 },  // #E63333
};

var GRID = {
  startX: 100,
  startY: 100,
  cols: 3,
  padding: 40,
  shapeWidth: 200,
  shapeHeight: 200,
};

// ── Helpers ──

function sendCommand(command, payload) {
  return new Promise(function(resolve, reject) {
    var msgId = Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
    var body = JSON.stringify({ id: msgId, command: command, payload: payload });
    var options = {
      hostname: 'localhost', port: 9199, path: '/send-command',
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) }
    };
    var req = http.request(options, function(res) {
      var data = '';
      res.on('data', function(chunk) { data += chunk; });
      res.on('end', function() {
        try { resolve(JSON.parse(data)); } catch(e) { resolve({ status: 'ok', data: { raw: data } }); }
      });
    });
    req.on('error', function(err) { reject(err); });
    req.write(body);
    req.end();
  });
}

function sleep(ms) { return new Promise(function(r) { setTimeout(r, ms); }); }

function gridPosition(index) {
  var col = index % GRID.cols;
  var row = Math.floor(index / GRID.cols);
  return {
    x: GRID.startX + col * (GRID.shapeWidth + GRID.padding),
    y: GRID.startY + row * (GRID.shapeHeight + GRID.padding),
  };
}

function hexToFigma(hex) {
  hex = hex.replace('#', '');
  return {
    r: parseInt(hex.substring(0, 2), 16) / 255,
    g: parseInt(hex.substring(2, 4), 16) / 255,
    b: parseInt(hex.substring(4, 6), 16) / 255,
  };
}

function toFills(color) {
  return [{ type: 'SOLID', color: color }];
}

// ── Shape Builders ──

/**
 * Build a createRectangle command payload.
 */
function rect(params) {
  return {
    command: 'createRectangle',
    payload: {
      x: params.x || 0, y: params.y || 0,
      width: params.width || GRID.shapeWidth,
      height: params.height || GRID.shapeHeight,
      fills: toFills(params.fillColor || COLORS.accent),
      cornerRadius: params.cornerRadius || 0,
      name: params.name || 'Rectangle',
    },
  };
}

/**
 * Build a createEllipse command payload.
 */
function ellipse(params) {
  return {
    command: 'createEllipse',
    payload: {
      x: params.x || 0, y: params.y || 0,
      width: params.width || GRID.shapeWidth,
      height: params.height || GRID.shapeHeight,
      fills: toFills(params.fillColor || COLORS.accent),
      name: params.name || 'Ellipse',
    },
  };
}

/**
 * Build a createFrame command payload.
 */
function frame(params) {
  return {
    command: 'createFrame',
    payload: {
      x: params.x || 0, y: params.y || 0,
      width: params.width || GRID.shapeWidth,
      height: params.height || GRID.shapeHeight,
      fills: toFills(params.fillColor || COLORS.surface),
      name: params.name || 'Frame',
      cornerRadius: params.cornerRadius || 12,
    },
  };
}

/**
 * Build a createText command payload.
 */
function text(params) {
  return {
    command: 'createText',
    payload: {
      x: params.x || 0, y: params.y || 0,
      characters: params.characters || 'Label',
      fontSize: params.fontSize || 16,
      fontName: params.fontName || { family: 'Inter', style: 'Regular' },
      fills: toFills(params.fillColor || COLORS.text),
      name: params.name || 'Text',
    },
  };
}

/**
 * Create a regular polygon with N sides using Figma plugin createPolygon command.
 * The plugin code.js needs to support 'createPolygon'.
 */
function polygon(params) {
  var sides = params.sides || 6;
  return {
    command: 'createPolygon',
    payload: {
      x: params.x || 0, y: params.y || 0,
      width: params.width || GRID.shapeWidth,
      height: params.height || GRID.shapeHeight,
      pointCount: sides,
      fills: toFills(params.fillColor || COLORS.accent),
      name: params.name || 'Polygon (' + sides + ' sides)',
    },
  };
}

/**
 * Create a star shape using Figma plugin createStar command.
 * The plugin code.js needs to support 'createStar'.
 */
function star(params) {
  var points = params.starPoints || 5;
  var innerRadius = params.innerRadius || 0.5;
  return {
    command: 'createStar',
    payload: {
      x: params.x || 0, y: params.y || 0,
      width: params.width || GRID.shapeWidth,
      height: params.height || GRID.shapeHeight,
      pointCount: points,
      innerRadius: innerRadius,
      fills: toFills(params.fillColor || COLORS.accent),
      name: params.name || 'Star (' + points + ' points)',
    },
  };
}

/**
 * Create a heart shape using VectorNetwork.
 * Standard bezier heart path mapped to Figma VectorNetwork format.
 */
function heart(params) {
  var w = params.width || GRID.shapeWidth;
  var h = params.height || GRID.shapeHeight;
  var S = w / 100; // scale based on desired width

  // Heart SVG path: M 50,18 C 35,0 0,15 0,42 C 0,65 25,82 50,98 C 75,82 100,65 100,42 C 100,15 65,0 50,18 Z
  // 4 cubic curves, 5 vertices (closing back to start)
  var vertices = [
    { x: 50 * S, y: 18 * S },  // v0: top center dip
    { x: 0 * S, y: 42 * S },   // v1: left lobe
    { x: 50 * S, y: 98 * S },  // v2: bottom tip
    { x: 100 * S, y: 42 * S }, // v3: right lobe
    { x: 50 * S, y: 18 * S },  // v4: back to top (closed)
  ];

  // Tangents are relative offsets from their endpoint vertex
  // C cx1,cy1 cx2,cy2 x,y → tangent at start = cx1 - v_start.x, tangent at end = cx2 - x
  var segments = [
    // v0 → v1: C 35,0 0,15 0,42
    { start: 0, end: 1, tangentStart: { x: (35 - 50) * S, y: (0 - 18) * S }, tangentEnd: { x: (0 - 0) * S, y: (15 - 42) * S } },
    // v1 → v2: C 0,65 25,82 50,98
    { start: 1, end: 2, tangentStart: { x: (0 - 0) * S, y: (65 - 42) * S }, tangentEnd: { x: (25 - 50) * S, y: (82 - 98) * S } },
    // v2 → v3: C 75,82 100,65 100,42
    { start: 2, end: 3, tangentStart: { x: (75 - 50) * S, y: (82 - 98) * S }, tangentEnd: { x: (100 - 100) * S, y: (65 - 42) * S } },
    // v3 → v4: C 100,15 65,0 50,18
    { start: 3, end: 4, tangentStart: { x: (100 - 100) * S, y: (15 - 42) * S }, tangentEnd: { x: (65 - 50) * S, y: (0 - 18) * S } },
  ];

  var fill = params.fillColor || COLORS.red;

  return {
    command: 'createVectorNetwork',
    payload: {
      x: params.x || 0, y: params.y || 0,
      width: w, height: h,
      vectorNetwork: { vertices: vertices, segments: segments },
      fills: [{ type: 'SOLID', color: fill }],
      strokes: [],
      strokeWeight: 0,
      strokeAlign: 'CENTER',
      name: params.name || 'Heart',
    },
  };
}

/**
 * Apply boolean operation on existing nodes.
 * Expects params { operation: 'UNION'|'SUBTRACT'|'INTERSECT'|'EXCLUDE', nodeIds: [id1, id2] }
 */
function booleanOp(params) {
  return {
    command: 'booleanOperation',
    payload: {
      operation: params.operation || 'UNION',
      nodeIds: params.nodeIds || [],
      name: params.name || 'Boolean ' + (params.operation || 'UNION'),
      fills: toFills(params.fillColor || COLORS.accent),
    },
  };
}

/**
 * Build a frame containing multiple shapes, then union them.
 */
function unionShape(params) {
  var children = params.children || [];
  var unionName = params.name || 'Union Shape';
  var fillColor = params.fillColor || COLORS.accent;

  var commands = [];

  // 1. Create each child shape
  var childIds = [];
  var childIndex = 0;
  children.forEach(function(child) {
    var cmd;
    switch (child.type) {
      case 'ellipse': cmd = ellipse(child); break;
      case 'rect': cmd = rect(child); break;
      case 'polygon': cmd = polygon(child); break;
      case 'star': cmd = star(child); break;
      default: cmd = rect(child); break;
    }
    cmd.payload.name = unionName + ' — part ' + (childIndex + 1);
    commands.push(cmd);
    childIds.push('__pending__');
    childIndex++;
  });

  // 2. Wait, then select all children and union
  // The union is done client-side by the plugin, so we return the shape creation
  // and the caller handles union via booleanOperation command.
  
  return {
    createCommands: commands,
    union: {
      command: 'booleanOperation',
      payload: { operation: 'UNION', name: unionName, fills: toFills(fillColor || COLORS.accent) }
    }
  };
}

// ── Grid Generator ──

/**
 * Generate a grid of shapes from an array of shape definitions.
 * Returns an array of command objects.
 */
function generateShapeGrid(shapes) {
  var commands = [];

  shapes.forEach(function(shapeDef, index) {
    var pos = gridPosition(index);

    // Merge position into shape params
    shapeDef.x = shapeDef.x != null ? shapeDef.x : pos.x;
    shapeDef.y = shapeDef.y != null ? shapeDef.y : pos.y;
    shapeDef.width = shapeDef.width || GRID.shapeWidth;
    shapeDef.height = shapeDef.height || GRID.shapeHeight;

    var cmd;
    switch (shapeDef.type) {
      case 'rect': case 'rectangle': cmd = rect(shapeDef); break;
      case 'ellipse': cmd = ellipse(shapeDef); break;
      case 'polygon': cmd = polygon(shapeDef); break;
      case 'star': cmd = star(shapeDef); break;
      case 'heart': cmd = heart(shapeDef); break;
      case 'frame': cmd = frame(shapeDef); break;
      case 'text': cmd = text(shapeDef); break;
      default: cmd = rect(shapeDef); break;
    }
    commands.push(cmd);
  });

  return commands;
}

// ── Execute Commands ──

async function executeCommands(commands) {
  var results = [];
  for (var i = 0; i < commands.length; i++) {
    var cmd = commands[i];
    try {
      var result = await sendCommand(cmd.command, cmd.payload);
      results.push({ index: i, command: cmd.command, name: cmd.payload.name, result: result });
      console.log('  [' + (i + 1) + '/' + commands.length + '] ' + cmd.command + ': ' + (cmd.payload.name || '') + ' → ' + result.status);
      await sleep(500); // avoid flooding the connector
    } catch (err) {
      results.push({ index: i, command: cmd.command, name: cmd.payload.name, error: err.message });
      console.log('  [' + (i + 1) + '/' + commands.length + '] ' + cmd.command + ': ERROR — ' + err.message);
    }
  }
  return results;
}

// ── Demo Commands ──

function demoBasic() {
  var shapes = [
    { type: 'rect', cornerRadius: 12, name: 'Rounded Rect', fills: toFills(COLORS.accent) },
    { type: 'rect', cornerRadius: 0, name: 'Square Rect', fills: toFills(COLORS.surface) },
    { type: 'ellipse', name: 'Circle', fills: toFills(COLORS.green) },
    { type: 'polygon', sides: 6, name: 'Hexagon', fills: toFills(COLORS.accent) },
    { type: 'star', starPoints: 5, innerRadius: 0.5, name: '5-Point Star', fills: toFills(COLORS.green) },
    { type: 'star', starPoints: 8, innerRadius: 0.4, name: '8-Point Star', fills: toFills(COLORS.red) },
    { type: 'heart', name: 'Heart', fills: toFills(COLORS.red) },
    { type: 'rect', cornerRadius: 8, name: 'Button', fills: toFills(COLORS.accent), width: 160, height: 48 },
    { type: 'ellipse', name: 'Pill', fills: toFills(COLORS.green), width: 160, height: 48 },
  ];

  // Adjust grid for first 6, put small ones on row 2
  shapes[7].x = 100;
  shapes[7].y = 460;
  shapes[8].x = 340;
  shapes[8].y = 460;
  shapes[8].width = 160;
  shapes[8].height = 48;

  return generateShapeGrid(shapes);
}

function demoUnion() {
  // Create two overlapping circles, then union them
  return [
    { command: 'createEllipse', payload: { x: 400, y: 200, width: 200, height: 200, fills: toFills(COLORS.accent), name: 'Circle A' } },
    { command: 'createEllipse', payload: { x: 500, y: 200, width: 200, height: 200, fills: toFills(COLORS.accent), name: 'Circle B' } },
  ];
}

// ── Main CLI ──

async function main() {
  var command = process.argv[2] || 'help';
  var commands = [];

  switch (command) {
    case 'generate':
      // Single shape from JSON payload
      var payload = process.argv[3];
      if (payload) {
        var params = JSON.parse(payload);
        commands.push(rect(params));
      }
      break;

    case 'grid':
      // Grid from JSON file or inline JSON array
      var source = process.argv[3];
      if (source) {
        var shapes;
        if (source.endsWith('.json')) {
          shapes = JSON.parse(require('fs').readFileSync(source, 'utf8'));
        } else {
          shapes = JSON.parse(source);
        }
        commands = generateShapeGrid(shapes);
      }
      break;

    case 'test-basic':
      commands = demoBasic();
      break;

    case 'test-union':
      commands = demoUnion();
      break;

    case 'test-heart':
      commands = [heart({ x: 300, y: 150, width: 200, height: 200 })];
      break;

    default:
      console.log('\nShape Generator — Figma plugin shape creation\n');
      console.log('Usage:');
      console.log('  node shape_generator.js <command>\n');
      console.log('Commands:');
      console.log('  generate <json>      — single shape');
      console.log('  grid <json|file>     — grid of shapes');
      console.log('  test-basic           — demo basic shapes');
      console.log('  test-union           — demo union operation');
      console.log('  test-heart           — demo heart shape\n');
      console.log('Shape params JSON format:');
      console.log('  {"type":"rect","width":200,"height":200,"cornerRadius":12,"fillColor":{"r":0.14,"g":0.49,"b":1}}');
      console.log('  {"type":"polygon","sides":6}');
      console.log('  {"type":"star","starPoints":5,"innerRadius":0.5}');
      console.log('  {"type":"heart"}');
      console.log('  {"type":"ellipse"}');
      console.log('  {"type":"frame","width":400,"height":300}');
      console.log('  {"type":"text","characters":"Hello"}');
      return;
  }

  if (commands.length === 0) {
    console.log('No commands to execute.');
    return;
  }

  console.log('Executing ' + commands.length + ' command(s)...\n');
  var results = await executeCommands(commands);
  console.log('\nDone. ' + results.filter(function(r) { return !r.error; }).length + '/' + results.length + ' succeeded.');
}

main().catch(function(err) { console.error('Error:', err.message); process.exit(1); });

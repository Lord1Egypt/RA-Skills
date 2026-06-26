// 02-design-system.js
// Example: Create a basic Design System component library
// Usage: Copy this code into your code.js, then run the plugin

var C = {
  n900:  { r: 0.10, g: 0.10, b: 0.11 },
  n700:  { r: 0.22, g: 0.22, b: 0.24 },
  n500:  { r: 0.44, g: 0.44, b: 0.47 },
  n300:  { r: 0.68, g: 0.68, b: 0.70 },
  n200:  { r: 0.82, g: 0.82, b: 0.84 },
  n100:  { r: 0.90, g: 0.90, b: 0.92 },
  n50:   { r: 0.96, g: 0.96, b: 0.97 },
  white: { r: 1.00, g: 1.00, b: 1.00 },
  p500:  { r: 0.90, g: 0.20, b: 0.20 },
  p100:  { r: 1.00, g: 0.88, b: 0.86 },
  s500:  { r: 0.20, g: 0.35, b: 0.70 },
  t500:  { r: 0.20, g: 0.65, b: 0.35 },
  e500:  { r: 0.90, g: 0.22, b: 0.21 },
};

function fill(c) { return { type: "SOLID", color: c }; }

function txt(content, size, weight, color) {
  var t = figma.createText();
  t.characters = content;
  t.fontSize = size;
  t.fontName = { family: "Inter", style: weight };
  t.fills = [fill(color)];
  return t;
}

async function main() {
  try {
    await figma.loadFontAsync({ family: "Inter", style: "Regular" });
    await figma.loadFontAsync({ family: "Inter", style: "Medium" });
    await figma.loadFontAsync({ family: "Inter", style: "Semi Bold" });
    await figma.loadFontAsync({ family: "Inter", style: "Bold" });

    var pages = figma.root.children;
    var target = pages[pages.length - 1];
    await figma.setCurrentPageAsync(target);

    var old = target.children.slice();
    for (var i = 0; i < old.length; i++) old[i].remove();

    // --- Color Swatches ---
    var section = figma.createFrame();
    section.name = "Colors";
    section.resize(500, 200);
    section.fills = [fill(C.white)];
    section.cornerRadius = 16;
    section.x = 0;
    section.y = 0;
    target.appendChild(section);

    var colors = [
      { name: "Primary", c: C.p500 },
      { name: "Secondary", c: C.s500 },
      { name: "Success", c: C.t500 },
      { name: "Error", c: C.e500 },
      { name: "N900", c: C.n900 },
      { name: "N500", c: C.n500 },
      { name: "N200", c: C.n200 },
      { name: "White", c: C.white },
    ];

    for (var ci = 0; ci < colors.length; ci++) {
      var swatch = figma.createRectangle();
      swatch.resize(48, 48);
      swatch.fills = [fill(colors[ci].c)];
      swatch.cornerRadius = 8;
      if (ci < 5) swatch.strokes = [fill(C.n200)];
      swatch.strokeWeight = 0.5;
      swatch.x = 20 + ci * 58;
      swatch.y = 20;
      section.appendChild(swatch);

      var label = txt(colors[ci].name, 9, "Regular", C.n500);
      label.x = 20 + ci * 58;
      label.y = 74;
      section.appendChild(label);
    }

    // --- Typography ---
    var typoSection = figma.createFrame();
    typoSection.name = "Typography";
    typoSection.resize(500, 300);
    typoSection.fills = [fill(C.white)];
    typoSection.cornerRadius = 16;
    typoSection.x = 0;
    typoSection.y = 220;
    target.appendChild(typoSection);

    var typeScale = [
      { name: "Title 1", size: 28, w: "Bold" },
      { name: "Title 2", size: 22, w: "Bold" },
      { name: "Title 3", size: 20, w: "Semi Bold" },
      { name: "Headline", size: 17, w: "Semi Bold" },
      { name: "Body", size: 17, w: "Regular" },
      { name: "Callout", size: 16, w: "Regular" },
      { name: "Subhead", size: 15, w: "Medium" },
      { name: "Footnote", size: 13, w: "Regular" },
      { name: "Caption", size: 12, w: "Medium" },
    ];

    var ty = 20;
    for (var ti = 0; ti < typeScale.length; ti++) {
      var ts = typeScale[ti];
      var label = txt(ts.name + " " + ts.size + "pt", 10, "Regular", C.n500);
      label.x = 20; label.y = ty;
      typoSection.appendChild(label);

      var sample = txt("The quick brown fox", ts.size, ts.w, C.n900);
      sample.x = 180; sample.y = ty - 2;
      typoSection.appendChild(sample);

      ty += 36;
    }

    // --- Buttons ---
    var btnSection = figma.createFrame();
    btnSection.name = "Buttons";
    btnSection.resize(500, 240);
    btnSection.fills = [fill(C.white)];
    btnSection.cornerRadius = 16;
    btnSection.x = 0;
    btnSection.y = 540;
    target.appendChild(btnSection);

    // Primary
    var b1 = figma.createFrame();
    b1.name = "Primary";
    b1.resize(300, 50);
    b1.cornerRadius = 25;
    b1.fills = [fill(C.p500)];
    b1.x = 20; b1.y = 20;
    btnSection.appendChild(b1);
    var b1t = txt("Primary Button", 17, "Semi Bold", C.white);
    b1t.resize(300, 50);
    b1t.textAlignHorizontal = "CENTER";
    b1t.textAlignVertical = "CENTER";
    b1.appendChild(b1t);

    // Secondary
    var b2 = figma.createFrame();
    b2.name = "Secondary";
    b2.resize(300, 50);
    b2.cornerRadius = 25;
    b2.fills = [fill(C.n100)];
    b2.x = 20; b2.y = 82;
    btnSection.appendChild(b2);
    var b2t = txt("Secondary Button", 17, "Semi Bold", C.n700);
    b2t.resize(300, 50);
    b2t.textAlignHorizontal = "CENTER";
    b2t.textAlignVertical = "CENTER";
    b2.appendChild(b2t);

    // Ghost
    var b3 = figma.createFrame();
    b3.name = "Ghost";
    b3.resize(300, 50);
    b3.cornerRadius = 25;
    b3.fills = [];
    b3.strokes = [fill(C.p500)];
    b3.strokeWeight = 2;
    b3.x = 20; b3.y = 144;
    btnSection.appendChild(b3);
    var b3t = txt("Ghost Button", 17, "Semi Bold", C.p500);
    b3t.resize(300, 50);
    b3t.textAlignHorizontal = "CENTER";
    b3t.textAlignVertical = "CENTER";
    b3.appendChild(b3t);

    figma.viewport.scrollAndZoomIntoView([section]);
    figma.notify("Design System created!", { timeout: 3000 });

  } catch (e) {
    figma.notify("ERROR: " + e.message, { timeout: 10000 });
  }
}

main();

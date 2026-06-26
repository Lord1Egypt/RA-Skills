// 01-basic-screen.js
// Example: Create a basic iOS-style screen
// Usage: Copy this code into your code.js, then run the plugin

async function main() {
  try {
    // Load fonts
    await figma.loadFontAsync({ family: "Inter", style: "Regular" });
    await figma.loadFontAsync({ family: "Inter", style: "Bold" });

    // Get the last page
    var pages = figma.root.children;
    var target = pages[pages.length - 1];
    await figma.setCurrentPageAsync(target);

    // Clear old content
    var old = target.children.slice();
    for (var i = 0; i < old.length; i++) old[i].remove();

    // Create screen background
    var screen = figma.createFrame();
    screen.name = "Home Screen";
    screen.resize(375, 812);
    screen.fills = [{ type: "SOLID", color: { r: 0.96, g: 0.96, b: 0.97 } }];
    screen.x = 0;
    screen.y = 0;
    target.appendChild(screen);

    // Status bar time
    var time = figma.createText();
    time.characters = "9:41";
    time.fontSize = 15;
    time.fontName = { family: "Inter", style: "Bold" };
    time.fills = [{ type: "SOLID", color: { r: 0, g: 0, b: 0 } }];
    time.x = 24;
    time.y = 12;
    screen.appendChild(time);

    // Title
    var title = figma.createText();
    title.characters = "Hello, World";
    title.fontSize = 34;
    title.fontName = { family: "Inter", style: "Bold" };
    title.fills = [{ type: "SOLID", color: { r: 0, g: 0, b: 0 } }];
    title.x = 20;
    title.y = 60;
    screen.appendChild(title);

    // Card
    var card = figma.createFrame();
    card.name = "Card";
    card.resize(335, 120);
    card.cornerRadius = 16;
    card.fills = [{ type: "SOLID", color: { r: 1, g: 1, b: 1 } }];
    card.effects = [{
      type: "DROP_SHADOW",
      color: { r: 0, g: 0, b: 0, a: 0.08 },
      offset: { x: 0, y: 4 },
      radius: 12,
      spread: 0,
      visible: true,
      blendMode: "NORMAL",
    }];
    card.x = 20;
    card.y = 120;
    screen.appendChild(card);

    // Card title
    var cardTitle = figma.createText();
    cardTitle.characters = "Welcome";
    cardTitle.fontSize = 20;
    cardTitle.fontName = { family: "Inter", style: "Bold" };
    cardTitle.fills = [{ type: "SOLID", color: { r: 0.1, g: 0.1, b: 0.1 } }];
    cardTitle.x = 20;
    cardTitle.y = 20;
    card.appendChild(cardTitle);

    // Card description
    var cardDesc = figma.createText();
    cardDesc.characters = "This is your first Figma plugin design.";
    cardDesc.fontSize = 14;
    cardDesc.fontName = { family: "Inter", style: "Regular" };
    cardDesc.fills = [{ type: "SOLID", color: { r: 0.5, g: 0.5, b: 0.5 } }];
    cardDesc.x = 20;
    cardDesc.y = 50;
    card.appendChild(cardDesc);

    // Button
    var btn = figma.createFrame();
    btn.name = "Button";
    btn.resize(335, 50);
    btn.cornerRadius = 25;
    btn.fills = [{ type: "SOLID", color: { r: 0.2, g: 0.4, b: 1.0 } }];
    btn.x = 20;
    btn.y = 260;
    screen.appendChild(btn);

    var btnText = figma.createText();
    btnText.characters = "Get Started";
    btnText.fontSize = 17;
    btnText.fontName = { family: "Inter", style: "Bold" };
    btnText.fills = [{ type: "SOLID", color: { r: 1, g: 1, b: 1 } }];
    btnText.resize(335, 50);
    btnText.textAlignHorizontal = "CENTER";
    btnText.textAlignVertical = "CENTER";
    btn.appendChild(btnText);

    // Done
    figma.viewport.scrollAndZoomIntoView([screen]);
    figma.notify("Screen created!", { timeout: 3000 });

  } catch (e) {
    figma.notify("ERROR: " + e.message, { timeout: 10000 });
  }
}

main();

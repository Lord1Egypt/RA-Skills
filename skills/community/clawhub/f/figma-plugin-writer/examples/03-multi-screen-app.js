// 03-multi-screen-app.js
// Example: Create a multi-screen iOS App prototype
// Usage: Copy this code into your code.js, then run the plugin

var SW = 375; // iPhone width
var SH = 812; // iPhone height

var C = {
  bg:    { r: 0.96, g: 0.96, b: 0.97 },
  white: { r: 1.00, g: 1.00, b: 1.00 },
  n900:  { r: 0.10, g: 0.10, b: 0.11 },
  n700:  { r: 0.22, g: 0.22, b: 0.24 },
  n500:  { r: 0.44, g: 0.44, b: 0.47 },
  n300:  { r: 0.68, g: 0.68, b: 0.70 },
  n200:  { r: 0.82, g: 0.82, b: 0.84 },
  n100:  { r: 0.90, g: 0.90, b: 0.92 },
  p500:  { r: 0.90, g: 0.20, b: 0.20 },
  p100:  { r: 1.00, g: 0.88, b: 0.86 },
  s500:  { r: 0.20, g: 0.35, b: 0.70 },
  t500:  { r: 0.20, g: 0.65, b: 0.35 },
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

function frame(name, w, h, color) {
  var f = figma.createFrame();
  f.name = name;
  f.resize(w, h);
  if (color) f.fills = [fill(color)];
  else f.fills = [];
  return f;
}

function tabBar(labels, activeIndex) {
  var tb = frame("Tab Bar", SW, 83, C.white);
  var border = figma.createRectangle();
  border.resize(SW, 0.5);
  border.fills = [fill(C.n200)];
  border.x = 0; border.y = 0;
  tb.appendChild(border);

  var tabW = SW / labels.length;
  for (var i = 0; i < labels.length; i++) {
    var isActive = i === activeIndex;
    var icon = figma.createRectangle();
    icon.resize(24, 24);
    icon.fills = [fill(isActive ? C.p500 : C.n300)];
    icon.x = i * tabW + (tabW - 24) / 2;
    icon.y = 12;
    tb.appendChild(icon);

    var label = txt(labels[i], 10, isActive ? "Semi Bold" : "Regular", isActive ? C.p500 : C.n500);
    label.textAlignHorizontal = "CENTER";
    label.x = i * tabW;
    label.y = 40;
    tb.appendChild(label);
  }
  return tb;
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

    var tabs = ["Home", "Explore", "Add", "Alerts", "Profile"];
    var gap = 60;

    // --- Screen 1: Home ---
    var s1 = frame("Home", SW, SH, C.bg);
    s1.x = 0; s1.y = 0;
    target.appendChild(s1);

    var t1 = txt("Home", 34, "Bold", C.n900);
    t1.x = 20; t1.y = 60;
    s1.appendChild(t1);

    // Search bar
    var search = frame("Search", SW - 40, 44, C.n100);
    search.cornerRadius = 12;
    search.x = 20; search.y = 110;
    s1.appendChild(search);
    var searchPh = txt("Search...", 16, "Regular", C.n300);
    searchPh.x = 16; searchPh.y = 12;
    search.appendChild(searchPh);

    // Featured card
    var featured = frame("Featured", SW - 40, 180, C.p500);
    featured.cornerRadius = 16;
    featured.x = 20; featured.y = 174;
    s1.appendChild(featured);
    var fTitle = txt("Featured Event", 24, "Bold", C.white);
    fTitle.x = 20; fTitle.y = 120;
    featured.appendChild(fTitle);
    var fSub = txt("Tap to explore", 14, "Regular", C.p100);
    fSub.x = 20; fSub.y = 150;
    featured.appendChild(fSub);

    // Section title
    var sec1 = txt("Recent", 20, "Bold", C.n900);
    sec1.x = 20; sec1.y = 374;
    s1.appendChild(sec1);

    // List items
    for (var li = 0; li < 3; li++) {
      var item = frame("Item " + (li + 1), SW - 40, 68, C.white);
      item.cornerRadius = 12;
      item.x = 20; item.y = 408 + li * 80;
      s1.appendChild(item);

      var icon = figma.createRectangle();
      icon.resize(40, 40);
      icon.fills = [fill([C.p100, C.n100, C.p100][li])];
      icon.cornerRadius = 10;
      icon.x = 14; icon.y = 14;
      item.appendChild(icon);

      var iTitle = txt(["Item One", "Item Two", "Item Three"][li], 16, "Medium", C.n900);
      iTitle.x = 70; iTitle.y = 18;
      item.appendChild(iTitle);

      var iSub = txt("Description here", 13, "Regular", C.n500);
      iSub.x = 70; iSub.y = 40;
      item.appendChild(iSub);
    }

    s1.appendChild(tabBar(tabs, 0));

    // --- Screen 2: Explore ---
    var s2 = frame("Explore", SW, SH, C.bg);
    s2.x = SW + gap; s2.y = 0;
    target.appendChild(s2);

    var t2 = txt("Explore", 34, "Bold", C.n900);
    t2.x = 20; t2.y = 60;
    s2.appendChild(t2);

    // Category pills
    var cats = ["All", "Music", "Art", "Tech", "Food"];
    for (var ci = 0; ci < cats.length; ci++) {
      var pill = frame(cats[ci], 72, 36, ci === 0 ? C.p500 : C.n100);
      pill.cornerRadius = 18;
      pill.x = 20 + ci * 80; pill.y = 110;
      s2.appendChild(pill);
      var pillT = txt(cats[ci], 14, ci === 0 ? "Semi Bold" : "Regular", ci === 0 ? C.white : C.n700);
      pillT.textAlignHorizontal = "CENTER";
      pillT.resize(72, 36);
      pillT.textAlignVertical = "CENTER";
      pill.appendChild(pillT);
    }

    // Grid cards
    for (var gi = 0; gi < 6; gi++) {
      var card = frame("Card " + (gi + 1), (SW - 52) / 2, 140, [C.p100, C.n100, C.p100, C.n100, C.p100, C.n100][gi]);
      card.cornerRadius = 12;
      card.x = 20 + (gi % 2) * ((SW - 52) / 2 + 12);
      card.y = 166 + Math.floor(gi / 2) * 156;
      s2.appendChild(card);

      var cTitle = txt("Event " + (gi + 1), 14, "Semi Bold", C.n900);
      cTitle.x = 12; cTitle.y = 100;
      card.appendChild(cTitle);
    }

    s2.appendChild(tabBar(tabs, 1));

    // --- Screen 3: Profile ---
    var s3 = frame("Profile", SW, SH, C.bg);
    s3.x = (SW + gap) * 2; s3.y = 0;
    target.appendChild(s3);

    var t3 = txt("Profile", 34, "Bold", C.n900);
    t3.x = 20; t3.y = 60;
    s3.appendChild(t3);

    // Avatar
    var avatar = frame("Avatar", 80, 80, C.p100);
    avatar.cornerRadius = 40;
    avatar.x = (SW - 80) / 2; avatar.y = 110;
    s3.appendChild(avatar);

    var aInit = txt("A", 32, "Bold", C.p500);
    aInit.textAlignHorizontal = "CENTER";
    aInit.resize(80, 80);
    aInit.textAlignVertical = "CENTER";
    avatar.appendChild(aInit);

    var userName = txt("Alex Johnson", 22, "Bold", C.n900);
    userName.textAlignHorizontal = "CENTER";
    userName.resize(SW, 28);
    userName.x = 0; userName.y = 204;
    s3.appendChild(userName);

    var userEmail = txt("alex@example.com", 14, "Regular", C.n500);
    userEmail.textAlignHorizontal = "CENTER";
    userEmail.resize(SW, 20);
    userEmail.x = 0; userEmail.y = 236;
    s3.appendChild(userEmail);

    // Settings list
    var settings = ["Notifications", "Privacy", "Language", "Help", "About"];
    for (var si = 0; si < settings.length; si++) {
      var sItem = frame(settings[si], SW - 40, 56, C.white);
      sItem.cornerRadius = 12;
      sItem.x = 20; sItem.y = 280 + si * 66;
      s3.appendChild(sItem);

      var sLabel = txt(settings[si], 16, "Medium", C.n900);
      sLabel.x = 20; sLabel.y = 18;
      sItem.appendChild(sLabel);

      var arrow = txt(">", 16, "Regular", C.n300);
      arrow.x = SW - 72; arrow.y = 18;
      sItem.appendChild(arrow);
    }

    s3.appendChild(tabBar(tabs, 4));

    figma.viewport.scrollAndZoomIntoView([s1]);
    figma.notify("3 screens created!", { timeout: 3000 });

  } catch (e) {
    figma.notify("ERROR: " + e.message, { timeout: 10000 });
  }
}

main();

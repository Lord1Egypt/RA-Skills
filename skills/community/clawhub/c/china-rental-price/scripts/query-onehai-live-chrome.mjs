#!/usr/bin/env node
import { execFile as execFileCallback } from "node:child_process";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { promisify } from "node:util";
import { normalizeQuery } from "./query.mjs";
import { splitLocalDateTime, nowIso } from "./utils.mjs";
import { extractPriceSignalsFromText, summarizeSignals } from "./extract.mjs";
import { buildOneHaiPeakRentalHint, parseOneHaiInventoryCount } from "./onehai-policy.mjs";

const execFile = promisify(execFileCallback);

function parseArgs(argv) {
  const args = {};
  for (let index = 0; index < argv.length; index += 1) {
    const part = argv[index];
    if (!part.startsWith("--")) {
      continue;
    }

    const key = part.slice(2).replace(/-([a-z])/g, (_, letter) => letter.toUpperCase());
    const next = argv[index + 1];
    if (!next || next.startsWith("--")) {
      args[key] = true;
      continue;
    }

    args[key] = next;
    index += 1;
  }
  return args;
}

function buildAppleScript(url, javascript, delaySeconds = 5) {
  return `
tell application "Google Chrome"
  if (count of windows) is 0 then
    make new window
  end if
  set targetTab to make new tab at end of tabs of front window with properties {URL:${JSON.stringify(url)}}
  delay ${delaySeconds}
  set scriptResult to execute targetTab javascript ${JSON.stringify(javascript)}
  close targetTab
  return scriptResult
end tell
`.trim();
}

async function runAppleScript(script) {
  try {
    const { stdout } = await execFile("osascript", ["-e", script], {
      encoding: "utf8",
      maxBuffer: 1024 * 1024 * 4
    });
    return stdout.trim();
  } catch (error) {
    const output = String(error.stderr || error.stdout || error.message || error);
    if (output.includes("通过 AppleScript 执行 JavaScript 的功能已关闭")) {
      throw new Error("Chrome 当前关闭了“允许 Apple 事件中的 JavaScript”，请先在 Chrome 菜单栏的“查看 > 开发者”中开启它。");
    }
    throw new Error(output.trim());
  }
}

function buildResolveBookingJavaScript(query) {
  const pickupTime = splitLocalDateTime(query.pickupAt);
  const dropoffTime = splitLocalDateTime(query.dropoffAt);

  return `
(function () {
  function appendFormValue(params, key, value) {
    if (value === undefined || value === null) {
      params.append(key, "");
      return;
    }
    if (typeof value === "object" && !Array.isArray(value)) {
      Object.keys(value).forEach(function (childKey) {
        appendFormValue(params, key + "[" + childKey + "]", value[childKey]);
      });
      return;
    }
    if (Array.isArray(value)) {
      value.forEach(function (item) {
        appendFormValue(params, key + "[]", item);
      });
      return;
    }
    params.append(key, String(value));
  }

  function post(url, data) {
    var xhr = new XMLHttpRequest();
    var params = new URLSearchParams();
    if (data && typeof data === "object") {
      Object.keys(data).forEach(function (key) {
        appendFormValue(params, key, data[key]);
      });
    }

    xhr.open("POST", url, false);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    xhr.send(params.toString());

    if (xhr.status < 200 || xhr.status >= 300) {
      throw new Error("HTTP " + xhr.status + " " + xhr.statusText);
    }

    return xhr.responseText;
  }

  function findCity(cityList, cityName) {
    return cityList.find(function (item) {
      return item.cityName === cityName;
    }) || null;
  }

  function pickStore(stores, locationHint) {
    if (!Array.isArray(stores) || stores.length === 0) {
      return null;
    }

    function scoreStore(store, scene, hint) {
      var text = [store.storeName, store.address, store.district].filter(Boolean).join(" ");
      var score = 0;

      if (hint && text.indexOf(hint) >= 0) {
        score += 10000;
      }

      if (scene === "train_station") {
        if (/高铁站/.test(text)) score += 600;
        if (/火车站/.test(text)) score += 520;
        if (/站内取还/.test(text)) score += 360;
        if (/客运/.test(text)) score -= 260;
        if (/机场/.test(text)) score -= 400;
      }

      if (scene === "airport") {
        if (/机场|航站楼|T1|T2|T3/.test(text)) score += 600;
        if (/高铁站|火车站/.test(text)) score -= 400;
      }

      if (/站内取还/.test(text)) score += 80;
      if (/店/.test(store.storeName || "")) score += 30;
      if (/自助点/.test(text)) score += 10;
      if (/停车场/.test(text)) score -= 12;
      if (/送车点/.test(text)) score -= 20;

      return score;
    }

    return stores.slice().sort(function (left, right) {
      return scoreStore(right, queryScene, locationHint) - scoreStore(left, queryScene, locationHint);
    })[0];
  }

  var cityList = JSON.parse(post("https://www.1hai.cn/Home/CityList", null)).data || [];
  var pickupCity = findCity(cityList, ${JSON.stringify(query.pickup.city)});
  var dropoffCity = findCity(cityList, ${JSON.stringify(query.dropoff.city)});
  if (!pickupCity) {
    return JSON.stringify({ ok: false, reason: "一嗨站内城市列表未找到 ${query.pickup.city}。" });
  }
  if (!dropoffCity) {
    return JSON.stringify({ ok: false, reason: "一嗨站内城市列表未找到 ${query.dropoff.city}。" });
  }

  var pickupStores = JSON.parse(post("https://www.1hai.cn/Premises/RegionalStore", { cityId: pickupCity.cityId })).data || [];
  var queryScene = ${JSON.stringify(query.pickup.scene)};
  var pickupStore = pickStore(pickupStores, ${JSON.stringify(query.pickup.location)});
  if (!pickupStore) {
    return JSON.stringify({ ok: false, reason: "${query.pickup.city} 当前未返回可预订门店。" });
  }

  var returnStore = pickupStore;
  if (${JSON.stringify(query.dropoff.city !== query.pickup.city || Boolean(query.dropoff.location))}) {
    var returnStores = JSON.parse(post("https://www.1hai.cn/Premises/RegionalStore", { cityId: dropoffCity.cityId })).data || [];
    queryScene = ${JSON.stringify(query.dropoff.scene)};
    returnStore = pickStore(returnStores, ${JSON.stringify(query.dropoff.location)});
    if (!returnStore) {
      return JSON.stringify({ ok: false, reason: "${query.dropoff.city} 当前未返回可预订还车门店。" });
    }
  }

  var redirectResponse = JSON.parse(post("https://www.1hai.cn/Home/RedirectFirstStep?v=" + Date.now(), {
    pickupDto: {
      pickUpCityId: String(pickupCity.cityId),
      getCarCity: pickupCity.cityName,
      getStoreId: String(pickupStore.id),
      getCarCityMenDian: pickupStore.storeName,
      txtGetCarAddress: "",
      getAddress: "",
      getCheck: false,
      pickUpTime: ${JSON.stringify(pickupTime.date)},
      pickUpHour: ${JSON.stringify(pickupTime.hour)},
      pickUpMinute: ${JSON.stringify(pickupTime.minute)},
      getLng: "",
      getLat: ""
    },
    returnDto: {
      returnCityId: String(dropoffCity.cityId),
      retCarCity: dropoffCity.cityName,
      retStoreId: String(returnStore.id),
      retCarCityMenDian: returnStore.storeName,
      txtDropCarAddress: "",
      retAddress: "",
      retCheck: false,
      returnTime: ${JSON.stringify(dropoffTime.date)},
      retHour: ${JSON.stringify(dropoffTime.hour)},
      returnMinute: ${JSON.stringify(dropoffTime.minute)},
      retLng: "",
      retLat: ""
    }
  }));

  if (!redirectResponse.success || !redirectResponse.data || !redirectResponse.data.redirectUrl) {
    return JSON.stringify({
      ok: false,
      reason: redirectResponse.message || "一嗨未返回选车页跳转地址。"
    });
  }

  return JSON.stringify({
    ok: true,
    bookingUrl: redirectResponse.data.redirectUrl,
    pickupStore: pickupStore.storeName,
    dropoffStore: returnStore.storeName
  });
})()
`.trim();
}

function buildReadBookingPageJavaScript() {
  return `
(function () {
  var vehicleCards = Array.from(document.querySelectorAll(".cartype-list")).map(function (card, index) {
    var canvas = card.querySelector(".cartype-price-current canvas");
    return {
      index: index + 1,
      text: (card.innerText || "").trim(),
      dataUrl: canvas ? canvas.toDataURL("image/png") : null
    };
  }).filter(function (item) {
    return item.dataUrl;
  });

  return JSON.stringify({
    url: location.href,
    title: document.title,
    bodyText: document.body.innerText,
    vehicleCards: vehicleCards
  });
})()
`.trim();
}

async function ocrCanvasDataUrl(dataUrl, outputPath) {
  const base64 = String(dataUrl || "").replace(/^data:image\/png;base64,/, "");
  await fs.writeFile(outputPath, Buffer.from(base64, "base64"));

  const { stdout } = await execFile("tesseract", [
    outputPath,
    "stdout",
    "--psm",
    "8",
    "-c",
    "tessedit_char_whitelist=0123456789"
  ], {
    encoding: "utf8",
    maxBuffer: 1024 * 1024
  });

  const digits = String(stdout || "").replace(/[^\d]/g, "");
  return digits ? Number(digits) : null;
}

function normalizeVehicleName(text) {
  const firstLine = String(text || "")
    .split(/\r?\n/)
    .map((line) => line.trim())
    .find(Boolean);

  if (!firstLine) {
    return null;
  }

  return firstLine.replace(/^(热门上新|长租特惠)\s*/u, "").trim() || null;
}

async function extractVehicleSamples(vehicleCards) {
  const tempDir = await fs.mkdtemp(path.join(os.tmpdir(), "onehai-live-"));
  const samples = [];

  try {
    for (const card of vehicleCards || []) {
      const outputPath = path.join(tempDir, `vehicle-${card.index}.png`);
      const price = await ocrCanvasDataUrl(card.dataUrl, outputPath).catch(() => null);
      if (price === null) {
        continue;
      }

      samples.push({
        index: card.index,
        vehicleName: normalizeVehicleName(card.text),
        priceDailyAverage: price
      });
    }
  } finally {
    await fs.rm(tempDir, { recursive: true, force: true }).catch(() => {});
  }

  return samples;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const query = normalizeQuery({
    pickupCity: args.pickupCity,
    pickupLocation: args.pickupLocation,
    pickupScene: args.pickupScene,
    dropoffCity: args.dropoffCity,
    dropoffLocation: args.dropoffLocation,
    dropoffScene: args.dropoffScene,
    pickupDateTime: args.pickupDatetime,
    dropoffDateTime: args.dropoffDatetime,
    vehicleClass: args.vehicleClass
  });

  const bookingRaw = await runAppleScript(buildAppleScript(
    "https://www.1hai.cn/index.aspx",
    buildResolveBookingJavaScript(query),
    5
  ));
  const booking = JSON.parse(bookingRaw);
  if (!booking.ok) {
    console.log(JSON.stringify({
      platform: "onehai-live-chrome",
      status: "fallback",
      capturedAt: nowIso(),
      query,
      warnings: [booking.reason]
    }, null, 2));
    return;
  }

  const bookingPageRaw = await runAppleScript(buildAppleScript(
    booking.bookingUrl,
    buildReadBookingPageJavaScript(),
    8
  ));
  const bookingPage = JSON.parse(bookingPageRaw);
  const inventoryCount = parseOneHaiInventoryCount(bookingPage.bodyText);
  const signals = extractPriceSignalsFromText(bookingPage.bodyText).filter((item) => {
    return !/元以下|元以上|\d+\s*-\s*\d+\s*元/.test(item.snippet);
  });
  const summary = summarizeSignals(signals);
  const requiresLogin = bookingPage.bodyText.includes("登录账户，即可查看库存与价格");
  const noCarsAvailable = inventoryCount === 0;
  const peakRentalHint = noCarsAvailable ? buildOneHaiPeakRentalHint(query, bookingPage.bodyText) : null;
  const vehicleSamples = noCarsAvailable ? [] : await extractVehicleSamples(bookingPage.vehicleCards);
  const priceMinFromVehicles = vehicleSamples.length
    ? Math.min(...vehicleSamples.map((item) => item.priceDailyAverage))
    : null;

  console.log(JSON.stringify({
    platform: "onehai-live-chrome",
    status: !requiresLogin && !noCarsAvailable && (summary.priceMin || priceMinFromVehicles) ? "priced" : "fallback",
    capturedAt: nowIso(),
    query,
    bookingUrl: booking.bookingUrl,
    selectedStore: {
      pickup: booking.pickupStore,
      dropoff: booking.dropoffStore
    },
    authMode: "live_chrome",
    priceMin: !noCarsAvailable ? (summary.priceMin ?? priceMinFromVehicles) : null,
    priceTotalIfAvailable: !noCarsAvailable ? (summary.priceTotalIfAvailable ?? priceMinFromVehicles) : null,
    availableCars: noCarsAvailable ? 0 : (inventoryCount ?? summary.availableCars),
    pricingUnit: !noCarsAvailable && (summary.pricingUnit || vehicleSamples.length) ? "day" : null,
    vehicleClass: summary.vehicleClass || query.vehicleClass,
    vehicleSamples,
    bookingRestriction: peakRentalHint,
    warnings: [
      ...(requiresLogin ? ["当前 Chrome 会话打开的一嗨选车页仍提示需要登录。"] : []),
      ...(noCarsAvailable ? [peakRentalHint?.warning || "当前选择的门店与时段暂无可租车型。"] : [])
    ],
    preview: bookingPage.bodyText.slice(0, 1200)
  }, null, 2));
}

main().catch((error) => {
  console.error(error.message || error);
  process.exitCode = 1;
});

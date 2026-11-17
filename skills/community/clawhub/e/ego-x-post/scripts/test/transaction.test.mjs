import assert from "node:assert/strict";
import test from "node:test";
import {
  animationKey,
  animationPathsFromHtml,
  buildTransactionId,
  decodeKeyBytes,
  describeMissingMaterials,
  encodeTransactionId,
  frameRowsFromPath,
  keyByteIndices,
  onDemandFileUrl,
  shellHasMaterials,
  verificationKeyFromHtml,
} from "../lib/transaction.mjs";

const HTML = `<meta content="AAAAAAAA" name="twitter-site-verification"><script>12:"ondemand.s" })[e]||e)+"."+({12:"h4sh"</script>`;
const PATH = "M 10 20 C 10 20 30 40 50 60 70 80 90 100 110 120 130";

test("page inputs parse, and a missing page does not invent an id", async () => {
  assert.equal(verificationKeyFromHtml(HTML), "AAAAAAAA");
  assert.equal(verificationKeyFromHtml(`<meta name="twitter-site-verification" content="abc+/=def">`), "abc+/=def");
  assert.equal(verificationKeyFromHtml("<html>"), "");
  assert.match(onDemandFileUrl(HTML), /ondemand\.s\.h4sha\.js$/);
  assert.equal(onDemandFileUrl("no chunk"), "");
  assert.equal(onDemandFileUrl('<script src="https://abs.twimg.com/responsive-web/client-web/ondemand.s.directHash.js"></script>'), "https://abs.twimg.com/responsive-web/client-web/ondemand.s.directHash.js");
  assert.equal(keyByteIndices("( n [ 12 ] , 16 )"), null);
  assert.deepEqual(keyByteIndices("(n[12], 16)(n[4], 16)(n[7], 16)"), { rowIndex: 12, keyBytesIndices: [4, 7] });
  assert.deepEqual(keyByteIndices(`return [1], 16${"x".repeat(200)}[38],16,[4], 16,[7],16;`), { rowIndex: 38, keyBytesIndices: [4, 7] });
  assert.equal(onDemandFileUrl(',20113:"ondemand.s",20113:"2c5bb94"'), "https://abs.twimg.com/responsive-web/client-web/ondemand.s.2c5bb94a.js");
  const svg = `<svg id="loading-x-anim-1"><g><path d="M0"/><path d="M 1 2 C 3 4 5 6 7 8 9"/></g></svg><svg id="loading-x-anim-0"><g><path d="M0"/><path d="M 9 9 C 1 1 2 2 3 3 4"/></g></svg>`;
  assert.deepEqual(animationPathsFromHtml(svg), ["M 9 9 C 1 1 2 2 3 3 4", "M 1 2 C 3 4 5 6 7 8 9"]);
  assert.equal(shellHasMaterials(`<meta name="twitter-site-verification" content="AAAAAAAA">${svg}<script src="https://abs.twimg.com/responsive-web/client-web/ondemand.s.directHash.js"></script>`), true);
  assert.deepEqual(describeMissingMaterials({ html: "<html></html>", ondemandSource: "", paths: [] }), ["twitter-site-verification", "ondemand.s url", "loading-x-anim"]);
  assert.deepEqual(keyByteIndices("(a[0], 16)(b[3], 16)"), { rowIndex: 0, keyBytesIndices: [3] });
  assert.equal(keyByteIndices("none"), null);
  assert.deepEqual(decodeKeyBytes(""), []);
  assert.equal(decodeKeyBytes("AAAAAAAA").length > 0, true);
  assert.deepEqual(frameRowsFromPath(""), []);
  assert.ok(frameRowsFromPath(PATH).length >= 1);
  assert.equal(animationKey([0], { rowIndex: 0, keyBytesIndices: [] }, [[1, 2]]), "");
  assert.equal(await buildTransactionId({ method: "POST", path: "/x", html: "", ondemandSource: "", paths: [] }), "");
  assert.equal(await encodeTransactionId({}), "");
});

test("a fixed clock and salt produce a stable transaction id", async () => {
  const keyBytes = decodeKeyBytes("AAAAAAAA");
  const rows = frameRowsFromPath(PATH);
  const key = animationKey(keyBytes, { rowIndex: 0, keyBytesIndices: [0, 0, 0, 0] }, rows);
  assert.equal(typeof key, "string");
  assert.ok(key.length > 4);
  const first = await encodeTransactionId({
    method: "POST",
    path: "/i/api/graphql/abc/CreateNoteTweet",
    keyBytes,
    animationKey: key,
    timeNow: 1000,
    randomByte: 7,
  });
  const second = await encodeTransactionId({
    method: "POST",
    path: "/i/api/graphql/abc/CreateNoteTweet",
    keyBytes,
    animationKey: key,
    timeNow: 1000,
    randomByte: 7,
  });
  assert.equal(first, second);
  assert.equal(first.includes("="), false);
  const id = await buildTransactionId({
    method: "POST",
    path: "/i/api/graphql/abc/CreateNoteTweet",
    html: HTML,
    ondemandSource: "(a[0], 16)(a[1], 16)(a[2], 16)(a[3], 16)",
    paths: [PATH, "", "", ""],
    timeNow: 50,
    randomByte: 9,
  });
  assert.equal(typeof id, "string");
  assert.ok(id.length > 8);
});

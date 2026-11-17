#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
const a = process.argv.slice(2),
  command = a[0],
  lib = a[a.indexOf("--with-library") + 1],
  file = path.join(lib, "fake.json");
const state = JSON.parse(fs.readFileSync(file, "utf8"));
state.calls.push(a);
state.stdin = fs.readFileSync(0, "utf8");
const save = () => fs.writeFileSync(file, JSON.stringify(state));
save();
if (command === "list") {
  const id = a[a.indexOf("--search") + 1].slice(3);
  const b = state.books[id];
  if (state.failRead) {
    console.error("synthetic read failure");
    process.exit(2);
  }
  console.log(JSON.stringify(b ? [b] : []));
} else if (command === "show_metadata") {
  const b = state.books[a.find((x) => /^[1-9][0-9]*$/.test(x))];
  const v = (b.title_sort || b.title).replaceAll("&", "&amp;").replaceAll('"', "&quot;");
  const authors = b.authors
    .replaceAll("&&", "\0")
    .split("&")
    .map((x) => x.replaceAll("\0", "&").trim());
  const creators = authors
    .map(
      (x) => "<dc:creator>" + x.replaceAll("&", "&amp;").replaceAll("<", "&lt;") + "</dc:creator>",
    )
    .join("");
  console.log(
    "<package>" + creators + '<meta name="calibre:title_sort" content="' + v + '"/></package>',
  );
} else if (command === "set_metadata") {
  state.sets++;
  save();
  if (state.failSet) {
    console.error("synthetic write failure");
    process.exit(2);
  }
  const b = state.books[a[1]];
  if (!b) process.exit(2);
  if (!state.lieSet)
    for (let i = 2; i < a.length; i++)
      if (a[i] === "--field") {
        const raw = a[++i],
          n = raw.indexOf(":"),
          k = raw.slice(0, n),
          v = raw.slice(n + 1);
        if (k === "tags") b.tags = v ? v.split(",") : [];
        else if (k === "languages")
          b.languages = v
            ? v.split(",").map((x) => ({ ja: "jpn", en: "eng", de: "deu" })[x] || x)
            : [];
        else if (k === "series_index") b[k] = Number(v);
        else b[k === "sort" ? "title_sort" : k] = v;
      }
  save();
  console.log("synthetic applied");
} else {
  console.error("unsupported fake command");
  process.exit(2);
}

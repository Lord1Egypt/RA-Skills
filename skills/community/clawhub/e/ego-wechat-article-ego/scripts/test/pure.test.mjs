import assert from "node:assert/strict";
import test from "node:test";
import {
  DIGEST_MAX,
  RESULT_TAG,
  TITLE_MAX,
  USAGE,
  buildArticle,
  clipDigest,
  decideAccount,
  decideSave,
  defaultReceiptDir,
  egoMissingSummary,
  escapeHtml,
  extractTaggedJson,
  formatResult,
  howToLogin,
  isForbiddenLabel,
  loginTip,
  normalizeText,
  parseCheckArgs,
  parseCleanupArgs,
  parseMarkdown,
  parseSaveArgs,
  planOf,
  redactUrl,
  resolveProcessExit,
  sniffImage,
  validateReadback,
} from "../lib/pure.mjs";

const sample = `---
title: "Git 存储"
description: "一段摘要"
tags: [git, github]
---

![封面](https://cdn.example/cover.jpg)

开头一段，带 **小听：** 和 \`Ref-CAS\`。

> 本文是说明。

- [原文](https://github.blog/post)
- 第二条

1. 先做这个
2. 再做那个

\`\`\`js
const n = 1;
\`\`\`

\`\`\`mermaid
graph TD
\`\`\`

## 参考链接

*图注一行*
`;

test("parsers accept help and reject keep, unknown flags, and a missing file", () => {
  assert.equal(parseCheckArgs(["--help"]).help, true);
  assert.equal(parseCheckArgs(["-h"]).help, true);
  assert.equal(parseCheckArgs(["--expect-account", "加选"]).expectAccount, "加选");
  assert.equal(parseCleanupArgs(["--json"]).json, true);
  assert.throws(() => parseCheckArgs(["--yes"]), /--yes/);
  assert.throws(() => parseCheckArgs(["--keep"]), /--keep/);
  assert.throws(() => parseSaveArgs(["--nope"]), /Unknown/);
  assert.throws(() => parseSaveArgs([]), /--markdown/);
  assert.throws(() => parseCheckArgs(["--markdown", "a.md"]), /save-draft/);
  const saved = parseSaveArgs([
    "--markdown=/absolute/path/article.md",
    "--yes",
    "--json",
    "--title", "标题",
    "--digest", "摘要",
    "--source-url", "https://example.com/p",
    "--asset-root", "/absolute/path/assets",
    "--expect-account=加选",
    "--receipt-dir", "/absolute/path/receipts",
    "--screenshot-dir", "/absolute/path/shots",
  ]);
  assert.equal(saved.yes, true);
  assert.equal(saved.markdown, "/absolute/path/article.md");
  assert.equal(saved.title, "标题");
  assert.match(USAGE, /--yes/);
  assert.throws(() => parseSaveArgs(["--title"]), /Missing value/);
});

test("markdown keeps structure, images, links, and code", () => {
  const parsed = parseMarkdown(sample);
  assert.equal(parsed.title, "Git 存储");
  assert.equal(parsed.description, "一段摘要");
  assert.equal(parsed.blocks.filter((block) => block.type === "image").length, 1);
  const quote = parsed.blocks.find((block) => block.type === "quote");
  assert.match(quote.text, /说明/);
  const list = parsed.blocks.find((block) => block.type === "list" && !block.ordered);
  assert.equal(list.items[0].links[0].href, "https://github.blog/post");
  assert.equal(parsed.blocks.some((block) => block.type === "list" && block.ordered), true);
  assert.equal(parsed.blocks.filter((block) => block.type === "code").length, 2);
  const heading = parsed.blocks.find((block) => block.type === "heading");
  assert.equal(heading.text, "参考链接");
  const noFront = parseMarkdown("# 只有标题\n\n正文");
  assert.equal(noFront.title, "只有标题");
  assert.equal(parseMarkdown("没有标题").title, "");
  assert.equal(parseMarkdown("---\ntitle: 未结束").blocks.length >= 0, true);
  assert.equal(normalizeText(" a \n b "), "a b");
  assert.equal(escapeHtml(`<a "&'>`), "&lt;a &quot;&amp;'&gt;");
});

test("buildArticle clips the digest, rejects a long title, and hashes images", () => {
  const parsed = parseMarkdown(sample);
  const images = [{ alt: "封面", name: "cover.jpg", path: "/absolute/path/cover.jpg", bytes: 4, sha256: "abc", remote: "https://cdn.example/cover.jpg" }];
  const built = buildArticle({ parsed, images, sourceUrl: "https://example.com/p" });
  assert.equal(built.ok, true);
  assert.equal(built.imageCount, 1);
  assert.equal(built.segments[0].kind, "image");
  const html = built.segments.filter((segment) => segment.kind === "html").map((segment) => segment.html).join("");
  assert.match(html, /<strong style="[^"]*font-weight:bold/);
  assert.match(html, /<h2 style="[^"]*border-bottom:2px solid rgb\(239,112,96\)/);
  assert.match(html, /background:rgb\(239,112,96\);color:#fff/);
  assert.match(html, /border-bottom:36px solid #efebe9;border-right:20px solid transparent/);
  assert.match(html, /<p style="font-size:16px;padding-top:8px;padding-bottom:8px;margin:0;line-height:26px;color:black;">/);
  assert.match(html, /<section style="[^"]*border-left:3px solid rgb\(239,112,96\)[^"]*background:#fff9f9/);
  assert.doesNotMatch(html, /<blockquote/);
  assert.match(html, />https:\/\/github\.blog\/post</);
  assert.doesNotMatch(html, />原文</);
  assert.match(html, /<span style="display:block;[^"]*word-break:break-all[^"]*">https:\/\/github\.blog\/post<\/span>/);
  assert.match(html, /<a href="https:\/\/github\.blog\/post" style="[^"]*text-decoration:none;border-bottom:1px solid #ef7060/);
  assert.ok(built.snippets.some((snippet) => snippet.includes("https://github.blog/post")));
  const caption = built.segments.find((segment) => segment.kind === "image").captionHtml;
  assert.match(caption, /<figcaption style="[^"]*margin-top:5px/);
  assert.match(caption, /padding:0/);
  assert.doesNotMatch(caption, /padding-top:8px/);
  assert.match(html, /<pre style="[^"]*border-radius:6px/);
  assert.doesNotMatch(html, /font-family:"/);
  assert.equal(built.fidelity.some((note) => note.includes("rgb(239,112,96)")), true);
  assert.equal(built.fidelity.some((note) => note.includes("mermaid")), true);
  assert.equal(built.hash.length, 64);
  const again = buildArticle({ parsed, images });
  assert.equal(again.hash, built.hash);
  assert.equal(clipDigest("短").trimmed, false);
  assert.equal([...clipDigest("字".repeat(DIGEST_MAX + 5)).text].length, DIGEST_MAX);
  const long = buildArticle({ parsed, images, title: "标".repeat(TITLE_MAX + 1) });
  assert.equal(long.ok, false);
  assert.match(long.error, /64/);
  const empty = buildArticle({ parsed: parseMarkdown("正文"), images: [] });
  assert.match(empty.error, /empty/);
  assert.match(buildArticle({ parsed, images: [] }).error, /image count/);
  const plan = planOf(built, "加选");
  assert.equal(plan.account, "加选");
  const sameLink = buildArticle({
    parsed: parseMarkdown("# 题\n\n![封面](https://cdn.example/cover.jpg)\n\n[https://example.com/a](https://example.com/a)\n"),
    images,
  });
  const sameHtml = sameLink.segments.filter((segment) => segment.kind === "html").map((segment) => segment.html).join("");
  assert.equal(sameHtml.split("https://example.com/a").length, 3);
  assert.doesNotMatch(sameHtml, />题</);
  assert.ok(sameLink.snippets.includes("https://example.com/a"));
  const refs = buildArticle({
    parsed: parseMarkdown("# 题\n\n![封面](https://cdn.example/cover.jpg)\n\n- [原文：Inside GitHub's new Git storage architecture](https://github.blog/engineering/architecture-optimization/inside-githubs-new-git-storage-architecture/)\n- [Hacker News 讨论](https://news.ycombinator.com/item?id=50397099)\n"),
    images,
  });
  const refText = refs.snippets.join("\n");
  assert.match(refText, /https:\/\/github\.blog\/engineering\/architecture-optimization\/inside-githubs-new-git-storage-architecture\//);
  assert.match(refText, /https:\/\/news\.ycombinator\.com\/item\?id=50397099/);
  const refHtml = refs.segments.filter((segment) => segment.kind === "html").map((segment) => segment.html).join("");
  assert.doesNotMatch(refHtml, /Inside GitHub/);
  assert.doesNotMatch(refHtml, /Hacker News/);
  assert.doesNotMatch(refHtml, /<h2[^>]*>题/);
  const titled = buildArticle({
    parsed: parseMarkdown("---\ntitle: 题\n---\n\n![题](https://cdn.example/cover.jpg)\n\n## 参考链接\n\n正文"),
    images,
  });
  assert.equal(titled.segments.find((segment) => segment.kind === "image").captionHtml, "");
  assert.match(titled.segments.filter((segment) => segment.kind === "html").map((segment) => segment.html).join(""), /参考链接/);
  assert.equal(plan.save, false);
});

test("account and save decisions stop before a second write", () => {
  assert.equal(decideAccount({ loginWall: true, loggedIn: false, accounts: [] }).reason, "logged-out");
  assert.equal(decideAccount(null).exitCode, 2);
  assert.equal(decideAccount({ loggedIn: true, accounts: ["甲", "乙"] }).reason, "ambiguous-account");
  assert.equal(decideAccount({ loggedIn: true, ambiguous: true, accounts: ["甲"] }).exitCode, 4);
  assert.equal(decideAccount({ loggedIn: true, accounts: [] }).reason, "unidentified-account");
  assert.equal(decideAccount({ loggedIn: true, accounts: ["甲"] }, "乙").reason, "account-mismatch");
  const ok = decideAccount({ loggedIn: true, accounts: ["甲"] }, "甲");
  assert.equal(ok.account, "甲");
  assert.equal(decideSave({ yes: false }).action, "dry-run");
  const saved = { hash: "h", status: "saved", draftId: "1" };
  assert.equal(decideSave({ yes: true, receipt: saved, hash: "h" }).action, "already-saved");
  assert.equal(decideSave({ yes: true, receipt: { hash: "h", status: "uncertain" }, hash: "h" }).action, "reconcile-first");
  assert.equal(decideSave({
    yes: true,
    receipt: { hash: "h", status: "pending" },
    draftsListed: true,
    drafts: [{ title: "题" }, { title: "题" }],
    hash: "h",
    title: "题",
  }).action, "ambiguous-draft");
  const reconciled = decideSave({
    yes: true,
    receipt: { hash: "h", status: "uncertain" },
    draftsListed: true,
    drafts: [{ title: "题", id: "9" }],
    hash: "h",
    title: "题",
  });
  assert.equal(reconciled.action, "reconciled");
  assert.equal(decideSave({
    yes: true,
    receipt: { hash: "h", status: "pending" },
    draftsListed: true,
    drafts: [],
    hash: "h",
    title: "题",
  }).reason, "reconciled-missing");
  assert.equal(decideSave({ yes: true, receipt: { hash: "h", status: "aborted" }, hash: "h" }).reason, "retry-aborted");
  assert.equal(decideSave({ yes: true, hash: "new" }).reason, "new");
});

test("readback, urls, images, and result formatting", () => {
  const expected = {
    title: "题",
    imageCount: 1,
    snippets: ["正文"],
    links: [{ href: "https://example.com/a", text: "链接" }],
  };
  const good = validateReadback(expected, {
    title: "题",
    text: "正文",
    imageCount: 1,
    hrefs: ["https://example.com/a"],
  });
  assert.equal(good.ok, true);
  assert.equal(good.missingHrefs.length, 0);
  const bad = validateReadback(expected, { title: "别的", text: "", imageCount: 0, hrefs: [] });
  assert.equal(bad.ok, false);
  assert.equal(bad.missingHrefs[0], "https://example.com/a");
  assert.equal(validateReadback({ ...expected, snippets: ["a"] }, { title: "题", text: "a", imageCount: 1, hrefs: [] }).missing.length, 0);
  assert.equal(redactUrl("https://mp.weixin.qq.com/cgi-bin/home?token=secret&t=home"), "https://mp.weixin.qq.com/cgi-bin/home?token=redacted&t=home");
  assert.equal(redactUrl("not a url"), "");
  assert.equal(sniffImage(Buffer.from([0xff, 0xd8, 0xff, 0x00])), "image/jpeg");
  assert.equal(sniffImage(Buffer.from([0x89, 0x50, 0x4e, 0x47, 0, 0, 0, 0])), "image/png");
  assert.equal(sniffImage(Buffer.from("GIF89aXXXX")), "image/gif");
  assert.equal(sniffImage(Buffer.from("RIFFXXXXWEBP")), "image/webp");
  assert.equal(sniffImage(Buffer.from("nope")), "");
  assert.equal(sniffImage(null), "");
  assert.equal(isForbiddenLabel("发表"), true);
  assert.equal(isForbiddenLabel("群发"), true);
  assert.equal(isForbiddenLabel("定时群发"), true);
  assert.equal(isForbiddenLabel("发送预览"), true);
  assert.equal(isForbiddenLabel("保存"), false);
  assert.equal(isForbiddenLabel("预览"), false);
  assert.equal(isForbiddenLabel(""), false);
  const summary = { exitCode: 0, saved: true, title: "题", account: "甲", draftId: "9" };
  assert.match(formatResult(summary), /saved 题/);
  assert.match(formatResult(summary, { asJson: true }), /"draftId": "9"/);
  assert.equal(formatResult(null), "");
  assert.match(formatResult({ exitCode: 3, saved: false }), /exitCode/);
  const packed = `noise\n${RESULT_TAG}${JSON.stringify({ exitCode: 3 })}\n`;
  assert.equal(extractTaggedJson(packed).exitCode, 3);
  assert.equal(extractTaggedJson(`${RESULT_TAG}{`), null);
  assert.equal(extractTaggedJson(""), null);
  assert.equal(resolveProcessExit("nodejs process exited with code 2", 0), 2);
  assert.equal(resolveProcessExit("", 0), 0);
  assert.equal(resolveProcessExit("", 1), 1);
  assert.match(defaultReceiptDir("/tmp/home"), /wechat-article-ego\/receipts/);
  assert.equal(defaultReceiptDir("/tmp/home", { WECHAT_ARTICLE_EGO_RECEIPT_DIR: "/absolute/path/receipts" }), "/absolute/path/receipts");
  assert.equal(defaultReceiptDir(""), "");
  assert.equal(howToLogin(["extra"]).how_to_login.at(-1), "extra");
  assert.match(loginTip("甲").login_tip_zh, /甲/);
  assert.match(egoMissingSummary("save-draft").error, /ego-browser/);
});

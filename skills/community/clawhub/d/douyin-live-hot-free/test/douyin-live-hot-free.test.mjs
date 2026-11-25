import test from "node:test";
import assert from "node:assert/strict";

import { buildSearchUrl, parseArgs, parseCount, renderHtml, renderMarkdown } from "../scripts/douyin-live-hot-free.mjs";

test("parses visible Douyin counts", () => {
  assert.equal(parseCount("11.3万"), 113_000);
  assert.equal(parseCount("1.5亿"), 150_000_000);
  assert.equal(parseCount("952"), 952);
  assert.equal(parseCount("unknown"), null);
});

test("builds an encoded Douyin Selected search URL", () => {
  assert.equal(buildSearchUrl("AI 工具"), "https://www.douyin.com/jingxuan/search/AI%20%E5%B7%A5%E5%85%B7?type=general");
});

test("parses search options", () => {
  assert.deepEqual(parseArgs(["search", "--keyword", "AI工具", "--browser", "自媒体", "--limit", "20", "--keep-tab"]), {
    verb: "search",
    options: { keyword: "AI工具", browser: "自媒体", limit: "20", keepTab: true },
  });
});

test("renders escaped search reports", () => {
  const data = {
    schemaVersion: "2.0",
    capturedAtLocal: "2026/08/30 20:00:00",
    source: { scope: "当前快照", url: "https://www.douyin.com/jingxuan/search/AI?type=general" },
    query: { keyword: "AI<工具>" },
    resultCount: 1,
    notice: "仅供研究",
    items: [{ position: 1, contentId: "1", contentType: "video", duration: "00:30", title: "<测试|作品>", visibleLikesText: "1万", author: "作者", publishedText: "今天", coverUrl: null, url: "https://www.douyin.com/video/1" }],
  };
  assert.match(renderMarkdown(data), /<测试\\\|作品>/);
  assert.match(renderHtml(data), /AI&lt;工具&gt;/);
  assert.match(renderHtml(data), /<!DOCTYPE html>/);
  assert.doesNotMatch(renderMarkdown(data), /排名|热度/);
});

import { createRequire } from "module";
const require2 = createRequire(import.meta.url);
globalThis.require = require2;
process.env.CC_SOUL_BENCHMARK = "1";
const { activationRecall } = require2("./activation-field.ts");
const { expandQuery, learnAssociation } = require2("./aam.ts");
const TEST_MEMORIES = [
  // ── 0-19: Original batch ──
  { content: "\u6211\u5728\u5B57\u8282\u8DF3\u52A8\u505A\u540E\u7AEF\u5F00\u53D1\uFF0C\u4E3B\u8981\u5199 Go \u8BED\u8A00", scope: "fact", ts: Date.now() - 864e5 * 30, confidence: 0.9, recallCount: 5, lastAccessed: Date.now() - 864e5 * 2 },
  { content: "\u6211\u5973\u670B\u53CB\u53EB\u5C0F\u96E8\uFF0C\u6211\u4EEC\u5728\u4E00\u8D77\u4E09\u5E74\u4E86", scope: "fact", ts: Date.now() - 864e5 * 60, confidence: 0.95, recallCount: 8, lastAccessed: Date.now() - 864e5 * 5 },
  { content: "\u6700\u8FD1\u8840\u538B\u6709\u70B9\u9AD8\uFF0C\u533B\u751F\u8BA9\u6211\u5C11\u5403\u76D0", scope: "fact", ts: Date.now() - 864e5 * 10, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - 864e5 * 3 },
  { content: "\u6211\u517B\u4E86\u4E00\u53EA\u6A58\u732B\u53EB\u6A58\u5B50\uFF0C\u7279\u522B\u80FD\u5403", scope: "fact", ts: Date.now() - 864e5 * 90, confidence: 0.9, recallCount: 6, lastAccessed: Date.now() - 864e5 * 1 },
  { content: "\u6211\u5927\u5B66\u5728\u6B66\u6C49\u8BFB\u7684\u8BA1\u7B97\u673A\u4E13\u4E1A", scope: "fact", ts: Date.now() - 864e5 * 120, confidence: 0.9, recallCount: 4, lastAccessed: Date.now() - 864e5 * 15 },
  { content: "\u53BB\u5E74\u5341\u4E00\u53BB\u4E86\u6210\u90FD\u65C5\u6E38\uFF0C\u5403\u4E86\u5F88\u591A\u706B\u9505", scope: "episode", ts: Date.now() - 864e5 * 180, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - 864e5 * 30 },
  { content: "\u6211\u6BCF\u5929\u65E9\u4E0A\u8DD1\u6B65 5 \u516C\u91CC\uFF0C\u575A\u6301\u4E86\u4E09\u4E2A\u6708", scope: "fact", ts: Date.now() - 864e5 * 45, confidence: 0.85, recallCount: 4, lastAccessed: Date.now() - 864e5 * 7 },
  { content: "\u6700\u8FD1\u5728\u5B66 Rust\uFF0C\u611F\u89C9\u6240\u6709\u6743\u7CFB\u7EDF\u5F88\u96BE\u7406\u89E3", scope: "fact", ts: Date.now() - 864e5 * 5, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - 864e5 * 1 },
  { content: "\u6211\u5988\u505A\u7684\u7EA2\u70E7\u8089\u7279\u522B\u597D\u5403\uFF0C\u6BCF\u6B21\u56DE\u5BB6\u90FD\u8981\u5403", scope: "fact", ts: Date.now() - 864e5 * 200, confidence: 0.9, recallCount: 3, lastAccessed: Date.now() - 864e5 * 20 },
  { content: "\u4E0A\u5468\u9762\u8BD5\u4E86\u963F\u91CC\u5DF4\u5DF4\uFF0C\u4E8C\u9762\u88AB\u5237\u4E86", scope: "episode", ts: Date.now() - 864e5 * 7, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 864e5 * 2 },
  { content: "\u6211\u6709\u8F7B\u5EA6\u5931\u7720\uFF0C\u4E00\u822C\u51CC\u6668\u4E00\u70B9\u624D\u80FD\u7761\u7740", scope: "fact", ts: Date.now() - 864e5 * 20, confidence: 0.8, recallCount: 3, lastAccessed: Date.now() - 864e5 * 5 },
  { content: "\u6B63\u5728\u8FD8\u623F\u8D37\uFF0C\u6BCF\u4E2A\u6708\u8FD8 8000", scope: "fact", ts: Date.now() - 864e5 * 60, confidence: 0.9, recallCount: 2, lastAccessed: Date.now() - 864e5 * 10 },
  { content: "\u5C0F\u96E8\u6000\u5B55\u4E86\uFF0C\u9884\u4EA7\u671F\u662F\u660E\u5E74\u4E09\u6708", scope: "fact", ts: Date.now() - 864e5 * 3, confidence: 0.95, recallCount: 5, lastAccessed: Date.now() - 864e5 * 1 },
  { content: "\u6211\u559C\u6B22\u770B\u79D1\u5E7B\u7535\u5F71\uFF0C\u6700\u559C\u6B22\u661F\u9645\u7A7F\u8D8A", scope: "preference", ts: Date.now() - 864e5 * 150, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 864e5 * 30 },
  { content: "\u5468\u672B\u7ECF\u5E38\u548C\u670B\u53CB\u6253\u7BEE\u7403\uFF0C\u5728\u516C\u53F8\u9644\u8FD1\u7684\u7403\u573A", scope: "fact", ts: Date.now() - 864e5 * 25, confidence: 0.8, recallCount: 3, lastAccessed: Date.now() - 864e5 * 3 },
  { content: "\u6211\u5BF9\u82B1\u7C89\u8FC7\u654F\uFF0C\u6625\u5929\u51FA\u95E8\u8981\u6234\u53E3\u7F69", scope: "fact", ts: Date.now() - 864e5 * 300, confidence: 0.9, recallCount: 4, lastAccessed: Date.now() - 864e5 * 60 },
  { content: "\u6700\u8FD1\u5728\u8003\u8651\u4E70\u7279\u65AF\u62C9 Model 3", scope: "fact", ts: Date.now() - 864e5 * 2, confidence: 0.75, recallCount: 1, lastAccessed: Date.now() - 864e5 * 1 },
  { content: "\u6211\u8001\u5BB6\u5728\u6E56\u5357\u957F\u6C99\uFF0C\u7279\u522B\u80FD\u5403\u8FA3", scope: "fact", ts: Date.now() - 864e5 * 365, confidence: 0.95, recallCount: 5, lastAccessed: Date.now() - 864e5 * 40 },
  { content: "\u4E0B\u4E2A\u6708\u8981\u53C2\u52A0\u670B\u53CB\u7684\u5A5A\u793C\uFF0C\u9700\u8981\u51C6\u5907\u4EFD\u5B50\u94B1", scope: "episode", ts: Date.now() - 864e5 * 1, confidence: 0.8, recallCount: 1, lastAccessed: Date.now() },
  { content: "\u6700\u8FD1\u7ECF\u5E38\u52A0\u73ED\u5230\u5341\u4E00\u70B9\uFF0C\u611F\u89C9\u5F88\u7D2F", scope: "episode", ts: Date.now() - 864e5 * 3, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - 864e5 * 1 },
  // ── 20-39: Second batch ──
  { content: "\u6211\u6BCF\u5929\u65E9\u4E0A 7 \u70B9\u8D77\u5E8A\u8DD1\u6B65", scope: "fact", ts: Date.now() - 864e5 * 15, confidence: 0.9, recallCount: 5, lastAccessed: Date.now() - 864e5 * 1 },
  { content: "\u6211\u5BF9\u82B1\u7C89\u8FC7\u654F\uFF0C\u6625\u5929\u4E0D\u80FD\u51FA\u95E8", scope: "fact", ts: Date.now() - 864e5 * 180, confidence: 0.9, recallCount: 4, lastAccessed: Date.now() - 864e5 * 30 },
  { content: "\u6211\u7684\u8F66\u662F\u7279\u65AF\u62C9 Model 3", scope: "fact", ts: Date.now() - 864e5 * 50, confidence: 0.92, recallCount: 3, lastAccessed: Date.now() - 864e5 * 5 },
  { content: "\u4E0A\u4E2A\u6708\u5DE5\u8D44\u6DA8\u4E86 2000", scope: "fact", ts: Date.now() - 864e5 * 35, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 864e5 * 10 },
  { content: "\u6211\u5973\u513F\u5728\u5B66\u94A2\u7434\uFF0C\u6BCF\u5468\u4E09\u4E0A\u8BFE", scope: "fact", ts: Date.now() - 864e5 * 60, confidence: 0.9, recallCount: 4, lastAccessed: Date.now() - 864e5 * 7 },
  { content: "\u6211\u6212\u70DF\u7B2C 47 \u5929\u4E86", scope: "fact", ts: Date.now() - 864e5 * 8, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - 864e5 * 2 },
  { content: "\u6211\u6700\u6015\u86C7", scope: "fact", ts: Date.now() - 864e5 * 120, confidence: 0.88, recallCount: 2, lastAccessed: Date.now() - 864e5 * 20 },
  { content: "\u4E0B\u4E2A\u6708\u8981\u53BB\u65E5\u672C\u65C5\u6E38", scope: "episode", ts: Date.now() - 864e5 * 5, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 864e5 * 1 },
  { content: "\u6211\u5927\u5B66\u5BA4\u53CB\u53EB\u5F20\u78CA\uFF0C\u73B0\u5728\u5728\u817E\u8BAF", scope: "fact", ts: Date.now() - 864e5 * 150, confidence: 0.88, recallCount: 3, lastAccessed: Date.now() - 864e5 * 25 },
  { content: "\u6211\u8840\u578B\u662F O \u578B", scope: "fact", ts: Date.now() - 864e5 * 200, confidence: 0.95, recallCount: 1, lastAccessed: Date.now() - 864e5 * 60 },
  { content: "\u5468\u672B\u4E00\u822C\u966A\u5B69\u5B50\u53BB\u516C\u56ED", scope: "fact", ts: Date.now() - 864e5 * 40, confidence: 0.85, recallCount: 4, lastAccessed: Date.now() - 864e5 * 3 },
  { content: "\u6211\u5728\u8003\u8651\u6362\u5DE5\u4F5C\uFF0C\u76EE\u6807\u662F\u963F\u91CC", scope: "fact", ts: Date.now() - 864e5 * 3, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 864e5 * 1 },
  { content: "\u6211\u7092\u80A1\u4E8F\u4E86 3 \u4E07", scope: "fact", ts: Date.now() - 864e5 * 25, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - 864e5 * 8 },
  { content: "\u6211\u6B63\u5728\u5B66\u65E5\u8BED\uFF0CN3 \u6C34\u5E73", scope: "fact", ts: Date.now() - 864e5 * 20, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - 864e5 * 4 },
  { content: "\u6211\u548C\u8001\u5A46\u662F\u5927\u5B66\u540C\u5B66", scope: "fact", ts: Date.now() - 864e5 * 170, confidence: 0.93, recallCount: 5, lastAccessed: Date.now() - 864e5 * 15 },
  { content: "\u6211\u7684 MacBook \u662F M2 Pro 32G", scope: "fact", ts: Date.now() - 864e5 * 45, confidence: 0.88, recallCount: 2, lastAccessed: Date.now() - 864e5 * 6 },
  { content: "\u6211\u6BCF\u5468\u4E94\u548C\u670B\u53CB\u6253\u7FBD\u6BDB\u7403", scope: "fact", ts: Date.now() - 864e5 * 30, confidence: 0.83, recallCount: 4, lastAccessed: Date.now() - 864e5 * 3 },
  { content: "\u6211\u6700\u8FD1\u5728\u770B\u300A\u4E09\u4F53\u300B", scope: "fact", ts: Date.now() - 864e5 * 10, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 864e5 * 2 },
  { content: "\u53BB\u5E74\u505A\u4E86\u8FD1\u89C6\u624B\u672F", scope: "fact", ts: Date.now() - 864e5 * 100, confidence: 0.9, recallCount: 1, lastAccessed: Date.now() - 864e5 * 40 },
  { content: "\u6211\u5728\u5B57\u8282\u505A\u5B89\u5168\u5DE5\u7A0B\u5E08", scope: "fact", ts: Date.now() - 864e5 * 12, confidence: 0.92, recallCount: 6, lastAccessed: Date.now() - 864e5 * 1 },
  // ── 40-79: New batch — social media, music, cooking, weather, childhood, goals, routines, shopping, transport, news ──
  // Social media / online habits (40-43)
  { content: "\u6211\u6BCF\u5929\u5237\u6296\u97F3\u81F3\u5C11\u4E24\u5C0F\u65F6", scope: "fact", ts: Date.now() - 864e5 * 20, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - 864e5 * 1 },
  { content: "\u6211\u6709\u4E00\u4E2A\u6280\u672F\u535A\u5BA2\uFF0C\u5199\u4E86 50 \u591A\u7BC7\u6587\u7AE0", scope: "fact", ts: Date.now() - 864e5 * 90, confidence: 0.88, recallCount: 2, lastAccessed: Date.now() - 864e5 * 10 },
  { content: "\u6211\u5FAE\u4FE1\u597D\u53CB\u6709 2000 \u591A\u4EBA", scope: "fact", ts: Date.now() - 864e5 * 60, confidence: 0.8, recallCount: 1, lastAccessed: Date.now() - 864e5 * 15 },
  { content: "\u6211\u5728\u5C0F\u7EA2\u4E66\u4E0A\u5173\u6CE8\u4E86\u5F88\u591A\u7F8E\u98DF\u535A\u4E3B", scope: "fact", ts: Date.now() - 864e5 * 30, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 864e5 * 5 },
  // Music preferences (44-47)
  { content: "\u6211\u6700\u559C\u6B22\u5468\u6770\u4F26\u7684\u6B4C\uFF0C\u542C\u4E86\u4E8C\u5341\u5E74\u4E86", scope: "preference", ts: Date.now() - 864e5 * 200, confidence: 0.92, recallCount: 5, lastAccessed: Date.now() - 864e5 * 3 },
  { content: "\u5199\u4EE3\u7801\u7684\u65F6\u5019\u4E60\u60EF\u542C lo-fi \u7535\u5B50\u4E50", scope: "fact", ts: Date.now() - 864e5 * 40, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - 864e5 * 2 },
  { content: "\u4E0A\u4E2A\u6708\u53BB\u770B\u4E86\u4E94\u6708\u5929\u7684\u6F14\u5531\u4F1A", scope: "episode", ts: Date.now() - 864e5 * 28, confidence: 0.88, recallCount: 2, lastAccessed: Date.now() - 864e5 * 7 },
  { content: "\u6211\u5C0F\u65F6\u5019\u5B66\u8FC7\u4E24\u5E74\u5C0F\u63D0\u7434\uFF0C\u540E\u6765\u6CA1\u575A\u6301", scope: "fact", ts: Date.now() - 864e5 * 250, confidence: 0.83, recallCount: 1, lastAccessed: Date.now() - 864e5 * 30 },
  // Cooking skills (48-51)
  { content: "\u6211\u4F1A\u505A\u7CD6\u918B\u6392\u9AA8\uFF0C\u662F\u6211\u7684\u62FF\u624B\u83DC", scope: "fact", ts: Date.now() - 864e5 * 50, confidence: 0.9, recallCount: 4, lastAccessed: Date.now() - 864e5 * 8 },
  { content: "\u6211\u505A\u996D\u57FA\u672C\u9760\u4E0B\u53A8\u623F App \u770B\u83DC\u8C31", scope: "fact", ts: Date.now() - 864e5 * 35, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 864e5 * 5 },
  { content: "\u4E0A\u5468\u5B66\u4F1A\u4E86\u505A\u63D0\u62C9\u7C73\u82CF", scope: "episode", ts: Date.now() - 864e5 * 6, confidence: 0.8, recallCount: 1, lastAccessed: Date.now() - 864e5 * 2 },
  { content: "\u6211\u4E0D\u5403\u9999\u83DC\uFF0C\u95FB\u5230\u5C31\u6076\u5FC3", scope: "preference", ts: Date.now() - 864e5 * 300, confidence: 0.95, recallCount: 4, lastAccessed: Date.now() - 864e5 * 10 },
  // Weather / seasonal preferences (52-55)
  { content: "\u6211\u6015\u51B7\uFF0C\u51AC\u5929\u4E0D\u613F\u610F\u51FA\u95E8", scope: "fact", ts: Date.now() - 864e5 * 120, confidence: 0.88, recallCount: 3, lastAccessed: Date.now() - 864e5 * 15 },
  { content: "\u6700\u559C\u6B22\u79CB\u5929\uFF0C\u4E0D\u51B7\u4E0D\u70ED\u521A\u521A\u597D", scope: "preference", ts: Date.now() - 864e5 * 150, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 864e5 * 20 },
  { content: "\u4E0B\u96E8\u5929\u5C31\u60F3\u5728\u5BB6\u6253\u6E38\u620F", scope: "fact", ts: Date.now() - 864e5 * 25, confidence: 0.8, recallCount: 3, lastAccessed: Date.now() - 864e5 * 4 },
  { content: "\u53BB\u5E74\u590F\u5929\u4E2D\u6691\u8FC7\u4E00\u6B21\uFF0C\u5728\u516C\u53F8\u6655\u5012\u4E86", scope: "episode", ts: Date.now() - 864e5 * 80, confidence: 0.87, recallCount: 2, lastAccessed: Date.now() - 864e5 * 25 },
  // Childhood memories (56-59)
  { content: "\u5C0F\u65F6\u5019\u5728\u519C\u6751\u957F\u5927\uFF0C\u7ECF\u5E38\u4E0B\u6CB3\u6478\u9C7C", scope: "fact", ts: Date.now() - 864e5 * 365, confidence: 0.9, recallCount: 3, lastAccessed: Date.now() - 864e5 * 40 },
  { content: "\u6211\u5C0F\u5B66\u7684\u65F6\u5019\u6570\u5B66\u7ADE\u8D5B\u62FF\u8FC7\u5E02\u4E00\u7B49\u5956", scope: "fact", ts: Date.now() - 864e5 * 350, confidence: 0.88, recallCount: 2, lastAccessed: Date.now() - 864e5 * 50 },
  { content: "\u6211\u4ECE\u5C0F\u5C31\u6015\u6253\u9488\uFF0C\u5230\u73B0\u5728\u8FD8\u662F", scope: "fact", ts: Date.now() - 864e5 * 280, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 864e5 * 35 },
  { content: "\u5C0F\u65F6\u5019\u517B\u8FC7\u4E00\u6761\u72D7\u53EB\u65FA\u8D22\uFF0C\u88AB\u8F66\u649E\u6B7B\u4E86", scope: "episode", ts: Date.now() - 864e5 * 400, confidence: 0.82, recallCount: 1, lastAccessed: Date.now() - 864e5 * 60 },
  // Future goals / dreams (60-63)
  { content: "\u6211\u7684\u68A6\u60F3\u662F\u5F00\u4E00\u5BB6\u5496\u5561\u5E97", scope: "fact", ts: Date.now() - 864e5 * 70, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - 864e5 * 12 },
  { content: "\u8BA1\u5212\u660E\u5E74\u8003 PMP \u9879\u76EE\u7BA1\u7406\u8BC1\u4E66", scope: "fact", ts: Date.now() - 864e5 * 15, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 864e5 * 3 },
  { content: "\u60F3\u5728 35 \u5C81\u4E4B\u524D\u6512\u591F 200 \u4E07", scope: "fact", ts: Date.now() - 864e5 * 45, confidence: 0.78, recallCount: 1, lastAccessed: Date.now() - 864e5 * 10 },
  { content: "\u6253\u7B97\u4E09\u5E74\u5185\u5728\u8001\u5BB6\u7ED9\u7236\u6BCD\u76D6\u4E00\u680B\u65B0\u623F\u5B50", scope: "fact", ts: Date.now() - 864e5 * 55, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - 864e5 * 8 },
  // Daily routines (64-67)
  { content: "\u6211\u65E9\u4E0A\u5148\u559D\u5496\u5561\u518D\u5403\u65E9\u996D", scope: "fact", ts: Date.now() - 864e5 * 30, confidence: 0.88, recallCount: 4, lastAccessed: Date.now() - 864e5 * 1 },
  { content: "\u4E2D\u5348\u4E00\u822C\u5728\u516C\u53F8\u98DF\u5802\u5403\u996D", scope: "fact", ts: Date.now() - 864e5 * 40, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - 864e5 * 2 },
  { content: "\u665A\u4E0A\u6D17\u5B8C\u6FA1\u4F1A\u770B\u534A\u5C0F\u65F6 B \u7AD9", scope: "fact", ts: Date.now() - 864e5 * 22, confidence: 0.82, recallCount: 3, lastAccessed: Date.now() - 864e5 * 1 },
  { content: "\u7761\u524D\u5FC5\u987B\u5237\u5341\u5206\u949F\u5FAE\u535A\u624D\u80FD\u5165\u7761", scope: "fact", ts: Date.now() - 864e5 * 18, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - 864e5 * 1 },
  // Shopping habits (68-71)
  { content: "\u6BCF\u4E2A\u6708\u82B1\u5728\u7F51\u8D2D\u4E0A\u5927\u6982 3000", scope: "fact", ts: Date.now() - 864e5 * 35, confidence: 0.83, recallCount: 2, lastAccessed: Date.now() - 864e5 * 5 },
  { content: "\u53CC\u5341\u4E00\u56E4\u4E86\u4E00\u5806\u96F6\u98DF\u548C\u65E5\u7528\u54C1", scope: "episode", ts: Date.now() - 864e5 * 140, confidence: 0.8, recallCount: 1, lastAccessed: Date.now() - 864e5 * 20 },
  { content: "\u4E70\u8863\u670D\u53EA\u5728\u4F18\u8863\u5E93\u548C Zara \u4E70", scope: "preference", ts: Date.now() - 864e5 * 80, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - 864e5 * 10 },
  { content: "\u6700\u8FD1\u8FF7\u4E0A\u4E86\u4E70\u76F2\u76D2\uFF0C\u5DF2\u7ECF\u82B1\u4E86\u4E00\u5343\u591A", scope: "fact", ts: Date.now() - 864e5 * 10, confidence: 0.78, recallCount: 2, lastAccessed: Date.now() - 864e5 * 3 },
  // Transportation (72-75)
  { content: "\u6211\u5750\u5730\u94C1\u4E0A\u73ED\uFF0C2 \u53F7\u7EBF\u8F6C 10 \u53F7\u7EBF", scope: "fact", ts: Date.now() - 864e5 * 50, confidence: 0.9, recallCount: 5, lastAccessed: Date.now() - 864e5 * 1 },
  { content: "\u4E0A\u73ED\u5355\u7A0B\u9700\u8981\u4E00\u4E2A\u534A\u5C0F\u65F6", scope: "fact", ts: Date.now() - 864e5 * 48, confidence: 0.88, recallCount: 3, lastAccessed: Date.now() - 864e5 * 2 },
  { content: "\u5076\u5C14\u9A91\u5171\u4EAB\u5355\u8F66\u53BB\u5730\u94C1\u7AD9", scope: "fact", ts: Date.now() - 864e5 * 30, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - 864e5 * 3 },
  { content: "\u53BB\u5E74\u62FF\u5230\u9A7E\u7167\u4E86\u4F46\u4E0D\u592A\u6562\u5F00\u8F66", scope: "fact", ts: Date.now() - 864e5 * 100, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 864e5 * 15 },
  // News / current events interests (76-79)
  { content: "\u6211\u5173\u6CE8\u79D1\u6280\u65B0\u95FB\uFF0C\u6BCF\u5929\u770B 36kr", scope: "fact", ts: Date.now() - 864e5 * 60, confidence: 0.87, recallCount: 4, lastAccessed: Date.now() - 864e5 * 1 },
  { content: "\u6700\u8FD1\u4E00\u76F4\u5728\u5173\u6CE8 AI \u5927\u6A21\u578B\u7684\u53D1\u5C55", scope: "fact", ts: Date.now() - 864e5 * 10, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - 864e5 * 1 },
  { content: "\u4E0D\u770B\u5A31\u4E50\u516B\u5366\uFF0C\u89C9\u5F97\u6D6A\u8D39\u65F6\u95F4", scope: "preference", ts: Date.now() - 864e5 * 90, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 864e5 * 12 },
  { content: "\u559C\u6B22\u770B B \u7AD9\u7684\u79D1\u666E\u89C6\u9891\uFF0C\u5173\u6CE8\u4E86\u534A\u4F5B\u4ED9\u4EBA", scope: "preference", ts: Date.now() - 864e5 * 55, confidence: 0.84, recallCount: 3, lastAccessed: Date.now() - 864e5 * 4 },
  // ── 80-99: Work details (项目/技术栈/同事/评价) ──
  { content: "\u6211\u8D1F\u8D23\u5B57\u8282\u5185\u90E8\u7684\u98CE\u63A7\u7CFB\u7EDF\uFF0C\u65E5\u5747\u5904\u7406 2 \u4EBF\u6761\u8BF7\u6C42", scope: "fact", ts: Date.now() - 864e5 * 20, confidence: 0.9, recallCount: 4, lastAccessed: Date.now() - 864e5 * 2 },
  { content: "\u6211\u4EEC\u7EC4\u7528\u7684\u6280\u672F\u6808\u662F Go + gRPC + Kafka + ClickHouse", scope: "fact", ts: Date.now() - 864e5 * 25, confidence: 0.88, recallCount: 3, lastAccessed: Date.now() - 864e5 * 3 },
  { content: "\u6211\u7684\u76F4\u5C5E leader \u53EB\u738B\u78CA\uFF0C\u4EBA\u5F88 nice \u4F46\u8981\u6C42\u5F88\u9AD8", scope: "fact", ts: Date.now() - 864e5 * 40, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 864e5 * 5 },
  { content: "\u4E0A\u4E2A\u5B63\u5EA6\u7EE9\u6548\u8BC4 B+\uFF0C\u5DEE\u4E00\u70B9\u62FF A", scope: "fact", ts: Date.now() - 864e5 * 15, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 864e5 * 3 },
  { content: "\u540C\u4E8B\u674E\u6668\u8DDF\u6211\u5173\u7CFB\u6700\u597D\uFF0C\u7ECF\u5E38\u4E00\u8D77\u5403\u5348\u996D", scope: "fact", ts: Date.now() - 864e5 * 35, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - 864e5 * 2 },
  { content: "\u516C\u53F8\u7ED9\u914D\u4E86\u4E24\u5757 4K \u663E\u793A\u5668\uFF0C\u529E\u516C\u4F53\u9A8C\u5F88\u597D", scope: "fact", ts: Date.now() - 864e5 * 50, confidence: 0.8, recallCount: 1, lastAccessed: Date.now() - 864e5 * 10 },
  { content: "\u6211\u4E4B\u524D\u5728\u7F8E\u56E2\u5E72\u4E86\u4E24\u5E74\uFF0C\u505A\u5916\u5356\u914D\u9001\u7B97\u6CD5", scope: "fact", ts: Date.now() - 864e5 * 200, confidence: 0.88, recallCount: 3, lastAccessed: Date.now() - 864e5 * 20 },
  { content: "\u5165\u804C\u5B57\u8282\u7684\u65F6\u5019\u5E74\u85AA\u6DA8\u4E86 40%", scope: "fact", ts: Date.now() - 864e5 * 180, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 864e5 * 15 },
  { content: "\u6211\u4EEC\u6BCF\u4E24\u5468\u4E00\u6B21 sprint review\uFF0C\u7EC4\u4F1A\u7528\u98DE\u4E66\u6587\u6863\u5199\u5468\u62A5", scope: "fact", ts: Date.now() - 864e5 * 30, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 864e5 * 4 },
  { content: "\u6700\u8FD1\u5728\u505A\u4E00\u4E2A\u53CD\u6B3A\u8BC8\u6A21\u578B\u7684 POC\uFF0C\u7528\u7684 Python + XGBoost", scope: "fact", ts: Date.now() - 864e5 * 5, confidence: 0.8, recallCount: 1, lastAccessed: Date.now() - 864e5 * 1 },
  { content: "\u5B9E\u4E60\u7684\u65F6\u5019\u5728\u767E\u5EA6\u505A\u8FC7\u641C\u7D22\u63A8\u8350", scope: "fact", ts: Date.now() - 864e5 * 300, confidence: 0.83, recallCount: 1, lastAccessed: Date.now() - 864e5 * 40 },
  { content: "\u516C\u53F8\u697C\u4E0B\u6709\u4E2A\u661F\u5DF4\u514B\uFF0C\u6211\u6BCF\u5929\u4E0B\u5348\u90FD\u53BB\u4E70\u4E00\u676F", scope: "fact", ts: Date.now() - 864e5 * 20, confidence: 0.8, recallCount: 3, lastAccessed: Date.now() - 864e5 * 1 },
  { content: "\u5B57\u8282\u7684\u5DE5\u4F4D\u662F\u5F00\u653E\u5F0F\u7684\uFF0C\u566A\u97F3\u5F88\u5927\u6234\u964D\u566A\u8033\u673A", scope: "fact", ts: Date.now() - 864e5 * 45, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 864e5 * 5 },
  { content: "\u4E0A\u4E2A\u6708\u63D0\u4E86\u4E00\u4E2A\u67B6\u6784\u4F18\u5316\u65B9\u6848\u88AB CTO \u8868\u626C\u4E86", scope: "episode", ts: Date.now() - 864e5 * 28, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 864e5 * 7 },
  { content: "\u540C\u4E8B\u5C0F\u9648\u521A\u79BB\u804C\u53BB\u4E86\u5FEB\u624B\uFF0C\u6211\u6709\u70B9\u52A8\u6447", scope: "episode", ts: Date.now() - 864e5 * 8, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - 864e5 * 2 },
  { content: "\u5E74\u5E95\u53EF\u80FD\u4F1A\u6709\u4E00\u6B21\u664B\u5347\u8BC4\u5BA1\uFF0C\u6211\u5728\u51C6\u5907\u8FF0\u804C PPT", scope: "fact", ts: Date.now() - 864e5 * 3, confidence: 0.82, recallCount: 1, lastAccessed: Date.now() - 864e5 * 1 },
  { content: "\u6211\u6709 3 \u5E74 Go \u7ECF\u9A8C\u30012 \u5E74 Python \u7ECF\u9A8C\u30011 \u5E74 Rust \u7ECF\u9A8C", scope: "fact", ts: Date.now() - 864e5 * 10, confidence: 0.9, recallCount: 3, lastAccessed: Date.now() - 864e5 * 2 },
  { content: "\u5B57\u8282\u7684\u798F\u5229\u5305\u62EC\u514D\u8D39\u4E09\u9910\u3001\u5065\u8EAB\u623F\u3001\u6BCF\u5E74\u4F53\u68C0", scope: "fact", ts: Date.now() - 864e5 * 60, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 864e5 * 15 },
  { content: "\u6211\u7684 GitHub \u6709 1200 \u4E2A star \u7684\u5F00\u6E90\u9879\u76EE", scope: "fact", ts: Date.now() - 864e5 * 80, confidence: 0.88, recallCount: 3, lastAccessed: Date.now() - 864e5 * 8 },
  { content: "\u516C\u53F8\u5E74\u4F1A\u62BD\u5956\u62BD\u5230\u4E86\u4E00\u53F0 iPad Pro", scope: "episode", ts: Date.now() - 864e5 * 120, confidence: 0.8, recallCount: 1, lastAccessed: Date.now() - 864e5 * 30 },
  // ── 100-119: Family details (父母/兄弟姐妹/家庭事件) ──
  { content: "\u6211\u7238\u662F\u4E2D\u5B66\u6570\u5B66\u8001\u5E08\uFF0C\u6559\u4E86\u4E09\u5341\u5E74\u4E66", scope: "fact", ts: Date.now() - 864e5 * 300, confidence: 0.92, recallCount: 3, lastAccessed: Date.now() - 864e5 * 20 },
  { content: "\u6211\u5988\u5728\u8D85\u5E02\u5F53\u6536\u94F6\u5458\uFF0C\u5FEB\u9000\u4F11\u4E86", scope: "fact", ts: Date.now() - 864e5 * 280, confidence: 0.9, recallCount: 2, lastAccessed: Date.now() - 864e5 * 25 },
  { content: "\u6211\u6709\u4E2A\u59B9\u59B9\u53EB\u5C0F\u654F\uFF0C\u6BD4\u6211\u5C0F\u56DB\u5C81\uFF0C\u5728\u6DF1\u5733\u505A\u8BBE\u8BA1", scope: "fact", ts: Date.now() - 864e5 * 250, confidence: 0.9, recallCount: 3, lastAccessed: Date.now() - 864e5 * 15 },
  { content: "\u59B9\u59B9\u53BB\u5E74\u7ED3\u5A5A\u4E86\uFF0C\u5AC1\u7ED9\u4E86\u5979\u5927\u5B66\u540C\u5B66", scope: "episode", ts: Date.now() - 864e5 * 150, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 864e5 * 30 },
  { content: "\u7237\u7237\u53BB\u5E74\u8FC7\u4E16\u4E86\uFF0C\u4EAB\u5E74 85 \u5C81", scope: "episode", ts: Date.now() - 864e5 * 200, confidence: 0.9, recallCount: 2, lastAccessed: Date.now() - 864e5 * 40 },
  { content: "\u5976\u5976\u8EAB\u4F53\u8FD8\u597D\uFF0C\u81EA\u5DF1\u4E00\u4E2A\u4EBA\u4F4F\u5728\u8001\u5BB6", scope: "fact", ts: Date.now() - 864e5 * 180, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 864e5 * 30 },
  { content: "\u8FC7\u5E74\u5168\u5BB6\u4EBA\u90FD\u56DE\u957F\u6C99\u8001\u5BB6\u56E2\u805A\uFF0C\u4E00\u822C\u521D\u4E09\u624D\u6563", scope: "fact", ts: Date.now() - 864e5 * 100, confidence: 0.88, recallCount: 3, lastAccessed: Date.now() - 864e5 * 60 },
  { content: "\u6211\u7238\u9AD8\u8840\u538B\u5403\u4E86\u5341\u51E0\u5E74\u836F\u4E86", scope: "fact", ts: Date.now() - 864e5 * 150, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 864e5 * 20 },
  { content: "\u5C0F\u96E8\u7684\u7236\u6BCD\u5728\u676D\u5DDE\uFF0C\u6BCF\u6B21\u53BB\u676D\u5DDE\u90FD\u4F4F\u5979\u5BB6", scope: "fact", ts: Date.now() - 864e5 * 90, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 864e5 * 15 },
  { content: "\u5BB6\u91CC\u7684\u623F\u5B50\u662F 2020 \u5E74\u4E70\u7684\uFF0C\u5728\u5317\u4EAC\u660C\u5E73\u56DE\u9F99\u89C2", scope: "fact", ts: Date.now() - 864e5 * 160, confidence: 0.9, recallCount: 3, lastAccessed: Date.now() - 864e5 * 10 },
  { content: "\u6211\u53D4\u53D4\u5728\u957F\u6C99\u5F00\u4E86\u4E00\u5BB6\u6E58\u83DC\u9986\uFF0C\u751F\u610F\u4E0D\u9519", scope: "fact", ts: Date.now() - 864e5 * 200, confidence: 0.82, recallCount: 1, lastAccessed: Date.now() - 864e5 * 35 },
  { content: "\u6211\u8868\u54E5\u5728\u90E8\u961F\u5F53\u5175\uFF0C\u662F\u4E2A\u8FDE\u957F", scope: "fact", ts: Date.now() - 864e5 * 220, confidence: 0.8, recallCount: 1, lastAccessed: Date.now() - 864e5 * 50 },
  { content: "\u6211\u5988\u7ECF\u5E38\u50AC\u6211\u8D76\u7D27\u7ED3\u5A5A\uFF0C\u6BCF\u6B21\u6253\u7535\u8BDD\u90FD\u63D0", scope: "fact", ts: Date.now() - 864e5 * 30, confidence: 0.85, recallCount: 4, lastAccessed: Date.now() - 864e5 * 5 },
  { content: "\u5C0F\u96E8\u548C\u6211\u5988\u5173\u7CFB\u4E0D\u9519\uFF0C\u8FC7\u5E74\u7ED9\u5979\u4E70\u4E86\u6761\u91D1\u9879\u94FE", scope: "fact", ts: Date.now() - 864e5 * 70, confidence: 0.83, recallCount: 2, lastAccessed: Date.now() - 864e5 * 10 },
  { content: "\u6211\u5F1F\uFF08\u8868\u5F1F\uFF09\u4ECA\u5E74\u9AD8\u8003\uFF0C\u76EE\u6807\u662F 985", scope: "fact", ts: Date.now() - 864e5 * 10, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 864e5 * 3 },
  { content: "\u6BCF\u5E74\u6E05\u660E\u8282\u56DE\u8001\u5BB6\u7ED9\u7237\u7237\u626B\u5893", scope: "fact", ts: Date.now() - 864e5 * 50, confidence: 0.8, recallCount: 1, lastAccessed: Date.now() - 864e5 * 20 },
  { content: "\u5BB6\u91CC\u517B\u4E86\u4E00\u6761\u91D1\u9C7C\u548C\u4E00\u76C6\u7EFF\u841D\uFF0C\u90FD\u662F\u5C0F\u96E8\u5728\u6253\u7406", scope: "fact", ts: Date.now() - 864e5 * 40, confidence: 0.78, recallCount: 1, lastAccessed: Date.now() - 864e5 * 8 },
  { content: "\u6211\u7238\u9000\u4F11\u540E\u8FF7\u4E0A\u4E86\u9493\u9C7C\uFF0C\u6BCF\u5468\u53BB\u4E09\u6B21", scope: "fact", ts: Date.now() - 864e5 * 15, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 864e5 * 3 },
  { content: "\u59B9\u59B9\u521A\u6000\u5B55\u4E24\u4E2A\u6708\uFF0C\u6211\u7238\u5988\u9AD8\u5174\u574F\u4E86", scope: "episode", ts: Date.now() - 864e5 * 5, confidence: 0.85, recallCount: 1, lastAccessed: Date.now() - 864e5 * 1 },
  { content: "\u6211\u548C\u5C0F\u96E8\u6253\u7B97\u660E\u5E74\u9886\u8BC1\uFF0C\u5A5A\u793C\u4ECE\u7B80", scope: "fact", ts: Date.now() - 864e5 * 8, confidence: 0.88, recallCount: 3, lastAccessed: Date.now() - 864e5 * 2 },
  // ── 120-139: Health / Finance / Education ──
  { content: "\u6211\u6709\u6162\u6027\u80C3\u708E\uFF0C\u4E0D\u80FD\u559D\u9152\u4E0D\u80FD\u5403\u8FA3\uFF08\u4F46\u8FD8\u662F\u5077\u5077\u5403\uFF09", scope: "fact", ts: Date.now() - 864e5 * 100, confidence: 0.88, recallCount: 3, lastAccessed: Date.now() - 864e5 * 10 },
  { content: "\u6BCF\u534A\u5E74\u53BB\u533B\u9662\u505A\u4E00\u6B21\u80C3\u955C\u68C0\u67E5", scope: "fact", ts: Date.now() - 864e5 * 60, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 864e5 * 15 },
  { content: "\u533B\u751F\u7ED9\u5F00\u4E86\u5965\u7F8E\u62C9\u5511\u548C\u83AB\u6C99\u5FC5\u5229\uFF0C\u6BCF\u5929\u996D\u524D\u5403", scope: "fact", ts: Date.now() - 864e5 * 50, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 864e5 * 8 },
  { content: "\u53BB\u5E74\u4F53\u68C0\u53D1\u73B0\u7532\u72B6\u817A\u7ED3\u8282\uFF0C\u533B\u751F\u8BF4\u5B9A\u671F\u590D\u67E5\u5C31\u884C", scope: "fact", ts: Date.now() - 864e5 * 120, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 864e5 * 20 },
  { content: "\u6211\u6709\u8170\u690E\u95F4\u76D8\u7A81\u51FA\uFF0C\u5750\u4E45\u4E86\u5C31\u75BC", scope: "fact", ts: Date.now() - 864e5 * 80, confidence: 0.87, recallCount: 3, lastAccessed: Date.now() - 864e5 * 5 },
  { content: "\u4E70\u4E86\u4E00\u628A Herman Miller \u4EBA\u4F53\u5DE5\u5B66\u6905\uFF0C\u82B1\u4E86\u516B\u5343\u591A", scope: "fact", ts: Date.now() - 864e5 * 70, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 864e5 * 10 },
  { content: "\u5728\u8682\u8681\u8D22\u5BCC\u4E0A\u4E70\u4E86 10 \u4E07\u7684\u8D27\u5E01\u57FA\u91D1", scope: "fact", ts: Date.now() - 864e5 * 90, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 864e5 * 12 },
  { content: "\u6BCF\u6708\u5B9A\u6295\u6CAA\u6DF1 300 \u6307\u6570\u57FA\u91D1 3000 \u5757", scope: "fact", ts: Date.now() - 864e5 * 75, confidence: 0.83, recallCount: 2, lastAccessed: Date.now() - 864e5 * 8 },
  { content: "\u4E70\u4E86\u767E\u4E07\u533B\u7597\u9669\u548C\u91CD\u75BE\u9669\uFF0C\u6BCF\u5E74\u4EA4 6000", scope: "fact", ts: Date.now() - 864e5 * 110, confidence: 0.85, recallCount: 1, lastAccessed: Date.now() - 864e5 * 25 },
  { content: "\u53BB\u5E74\u9000\u7A0E\u9000\u4E86 4800 \u5757", scope: "episode", ts: Date.now() - 864e5 * 130, confidence: 0.8, recallCount: 1, lastAccessed: Date.now() - 864e5 * 30 },
  { content: "\u516C\u79EF\u91D1\u6BCF\u4E2A\u6708\u4EA4 3200\uFF0C\u6253\u7B97\u4EE5\u540E\u63D0\u53D6\u51FA\u6765\u8FD8\u623F\u8D37", scope: "fact", ts: Date.now() - 864e5 * 55, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 864e5 * 10 },
  { content: "\u6B66\u6C49\u5927\u5B66\u8BA1\u7B97\u673A\u5B66\u9662\uFF0C\u5927\u4E09\u62FF\u8FC7\u56FD\u5BB6\u5956\u5B66\u91D1", scope: "fact", ts: Date.now() - 864e5 * 280, confidence: 0.9, recallCount: 2, lastAccessed: Date.now() - 864e5 * 35 },
  { content: "\u6BD5\u4E1A\u8BBE\u8BA1\u505A\u7684\u662F\u57FA\u4E8E\u6DF1\u5EA6\u5B66\u4E60\u7684\u4EBA\u8138\u8BC6\u522B\u7CFB\u7EDF", scope: "fact", ts: Date.now() - 864e5 * 260, confidence: 0.85, recallCount: 1, lastAccessed: Date.now() - 864e5 * 40 },
  { content: "\u5927\u5B66\u7684\u6570\u636E\u7ED3\u6784\u8001\u5E08\u59D3\u5468\uFF0C\u8BB2\u8BFE\u7279\u522B\u597D", scope: "fact", ts: Date.now() - 864e5 * 270, confidence: 0.82, recallCount: 1, lastAccessed: Date.now() - 864e5 * 45 },
  { content: "\u8003\u7814\u8003\u4E86\u4E24\u6B21\uFF0C\u7B2C\u4E00\u6B21\u5DEE 3 \u5206\u6CA1\u8FC7\u7EBF", scope: "fact", ts: Date.now() - 864e5 * 240, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 864e5 * 50 },
  { content: "\u540E\u6765\u653E\u5F03\u8003\u7814\u76F4\u63A5\u5DE5\u4F5C\u4E86\uFF0C\u73B0\u5728\u60F3\u60F3\u4E5F\u4E0D\u540E\u6094", scope: "fact", ts: Date.now() - 864e5 * 230, confidence: 0.82, recallCount: 1, lastAccessed: Date.now() - 864e5 * 45 },
  { content: "\u9AD8\u4E2D\u5728\u957F\u6C99\u4E00\u4E2D\u8BFB\u7684\uFF0C\u73ED\u4E3B\u4EFB\u59D3\u5218\uFF0C\u5BF9\u6211\u5F71\u54CD\u5F88\u5927", scope: "fact", ts: Date.now() - 864e5 * 350, confidence: 0.88, recallCount: 2, lastAccessed: Date.now() - 864e5 * 55 },
  { content: "\u4FE1\u7528\u5361\u989D\u5EA6 5 \u4E07\uFF0C\u4E00\u822C\u7528\u5230\u4E00\u534A\u5DE6\u53F3", scope: "fact", ts: Date.now() - 864e5 * 65, confidence: 0.8, recallCount: 1, lastAccessed: Date.now() - 864e5 * 12 },
  { content: "\u5728\u817E\u8BAF\u7406\u8D22\u901A\u8FD8\u6709 5 \u4E07\u5B9A\u671F\u5B58\u6B3E", scope: "fact", ts: Date.now() - 864e5 * 85, confidence: 0.83, recallCount: 1, lastAccessed: Date.now() - 864e5 * 15 },
  { content: "\u6BCF\u4E2A\u6708\u5230\u624B\u5DE5\u8D44\u5927\u6982 2.8 \u4E07", scope: "fact", ts: Date.now() - 864e5 * 30, confidence: 0.88, recallCount: 3, lastAccessed: Date.now() - 864e5 * 5 },
  // ── 140-159: Social / Hobbies / Daily routine details ──
  { content: "\u9AD8\u4E2D\u540C\u5B66\u7FA4\u91CC\u6700\u6D3B\u8DC3\u7684\u662F\u8001\u8D75\uFF0C\u6BCF\u5929\u53D1\u6BB5\u5B50", scope: "fact", ts: Date.now() - 864e5 * 100, confidence: 0.78, recallCount: 1, lastAccessed: Date.now() - 864e5 * 15 },
  { content: "\u5927\u5B66\u597D\u54E5\u4EEC\u5218\u6BC5\u5728\u6DF1\u5733\u521B\u4E1A\u505A SaaS\uFF0C\u7ECF\u5E38\u627E\u6211\u804A\u6280\u672F", scope: "fact", ts: Date.now() - 864e5 * 80, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 864e5 * 10 },
  { content: "\u6BCF\u4E2A\u6708\u548C\u5927\u5B66\u540C\u5B66\u7EBF\u4E0A\u6253\u4E00\u6B21\u72FC\u4EBA\u6740", scope: "fact", ts: Date.now() - 864e5 * 40, confidence: 0.82, recallCount: 3, lastAccessed: Date.now() - 864e5 * 5 },
  { content: "\u6211\u7684\u90BB\u5C45\u662F\u4E00\u5BF9\u9000\u4F11\u592B\u5987\uFF0C\u7ECF\u5E38\u9001\u6211\u4EEC\u81EA\u5DF1\u79CD\u7684\u83DC", scope: "fact", ts: Date.now() - 864e5 * 60, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - 864e5 * 8 },
  { content: "\u53BB\u5E74\u53C2\u52A0\u4E86\u516C\u53F8\u7684\u9ED1\u5BA2\u9A6C\u62C9\u677E\uFF0C\u62FF\u4E86\u4E8C\u7B49\u5956", scope: "episode", ts: Date.now() - 864e5 * 140, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 864e5 * 20 },
  { content: "\u6211\u5728 LeetCode \u4E0A\u5237\u4E86 600 \u591A\u9053\u9898", scope: "fact", ts: Date.now() - 864e5 * 90, confidence: 0.88, recallCount: 2, lastAccessed: Date.now() - 864e5 * 10 },
  { content: "\u6700\u8FD1\u8FF7\u4E0A\u4E86\u673A\u68B0\u952E\u76D8\uFF0C\u5DF2\u7ECF\u4E70\u4E86\u4E09\u628A\u4E86", scope: "fact", ts: Date.now() - 864e5 * 12, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 864e5 * 3 },
  { content: "\u559C\u6B22\u73A9\u539F\u795E\uFF0C\u96F7\u7535\u5C06\u519B\u6EE1\u547D\u4E86", scope: "fact", ts: Date.now() - 864e5 * 50, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - 864e5 * 4 },
  { content: "\u6BCF\u5468\u65E5\u4E0B\u5348\u53BB\u697C\u4E0B\u5496\u5561\u9986\u770B\u4E66\u4E24\u5C0F\u65F6", scope: "fact", ts: Date.now() - 864e5 * 25, confidence: 0.82, recallCount: 3, lastAccessed: Date.now() - 864e5 * 3 },
  { content: "\u65E9\u4E0A 6:50 \u95F9\u949F\u54CD\uFF0C\u8D56\u5E8A\u5341\u5206\u949F", scope: "fact", ts: Date.now() - 864e5 * 18, confidence: 0.85, recallCount: 4, lastAccessed: Date.now() - 864e5 * 1 },
  { content: "\u4ECE\u5BB6\u8D70\u5230\u5730\u94C1\u7AD9\u8981 15 \u5206\u949F", scope: "fact", ts: Date.now() - 864e5 * 35, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 864e5 * 2 },
  { content: "\u5348\u4F11\u4E00\u822C\u8DB4\u5728\u684C\u4E0A\u7761\u534A\u5C0F\u65F6", scope: "fact", ts: Date.now() - 864e5 * 28, confidence: 0.8, recallCount: 3, lastAccessed: Date.now() - 864e5 * 1 },
  { content: "\u6BCF\u5929\u4E0B\u5348\u4E09\u70B9\u559D\u676F\u5496\u5561\u7EED\u547D", scope: "fact", ts: Date.now() - 864e5 * 22, confidence: 0.82, recallCount: 3, lastAccessed: Date.now() - 864e5 * 1 },
  { content: "\u665A\u996D\u7ECF\u5E38\u70B9\u5916\u5356\uFF0C\u6700\u5E38\u70B9\u7684\u662F\u9EC4\u7116\u9E21", scope: "fact", ts: Date.now() - 864e5 * 15, confidence: 0.8, recallCount: 3, lastAccessed: Date.now() - 864e5 * 2 },
  { content: "\u6D17\u5B8C\u6FA1\u4E60\u60EF\u7528\u5439\u98CE\u673A\u628A\u5934\u53D1\u5B8C\u5168\u5439\u5E72", scope: "fact", ts: Date.now() - 864e5 * 20, confidence: 0.75, recallCount: 1, lastAccessed: Date.now() - 864e5 * 3 },
  { content: "\u6BCF\u5929\u665A\u4E0A\u5341\u70B9\u534A\u5F00\u59CB\u6D17\u6F31", scope: "fact", ts: Date.now() - 864e5 * 16, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - 864e5 * 1 },
  { content: "\u5065\u8EAB\u623F\u529E\u4E86\u5E74\u5361\u4F46\u53EA\u53BB\u4E86\u4E94\u6B21", scope: "fact", ts: Date.now() - 864e5 * 70, confidence: 0.78, recallCount: 1, lastAccessed: Date.now() - 864e5 * 15 },
  { content: "\u6211\u559C\u6B22\u62CD\u7167\uFF0C\u624B\u673A\u91CC\u6709 2 \u4E07\u591A\u5F20\u7167\u7247", scope: "fact", ts: Date.now() - 864e5 * 55, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 864e5 * 5 },
  { content: "\u6700\u8FD1\u5728\u7528 Notion \u505A\u4E2A\u4EBA\u77E5\u8BC6\u7BA1\u7406", scope: "fact", ts: Date.now() - 864e5 * 8, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - 864e5 * 2 },
  { content: "\u6BCF\u5468\u4E09\u665A\u4E0A\u548C\u5C0F\u96E8\u4E00\u8D77\u770B\u7EFC\u827A", scope: "fact", ts: Date.now() - 864e5 * 20, confidence: 0.82, recallCount: 3, lastAccessed: Date.now() - 864e5 * 3 },
  // ── 160-179: Personality / Life events / Travel ──
  { content: "\u6211\u813E\u6C14\u6BD4\u8F83\u6025\uFF0C\u8BF4\u8BDD\u76F4\u6765\u76F4\u53BB\u5BB9\u6613\u5F97\u7F6A\u4EBA", scope: "fact", ts: Date.now() - 864e5 * 150, confidence: 0.88, recallCount: 3, lastAccessed: Date.now() - 864e5 * 10 },
  { content: "\u9047\u5230\u4E0D\u516C\u5E73\u7684\u4E8B\u60C5\u4F1A\u5F53\u9762\u8BF4\u51FA\u6765\uFF0C\u4E0D\u4F1A\u618B\u7740", scope: "fact", ts: Date.now() - 864e5 * 130, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 864e5 * 12 },
  { content: "\u51B3\u5B9A\u4E70\u4EC0\u4E48\u4E1C\u897F\u4E4B\u524D\u4F1A\u505A\u5927\u91CF\u529F\u8BFE\uFF0C\u770B\u6D4B\u8BC4\u5BF9\u6BD4", scope: "fact", ts: Date.now() - 864e5 * 80, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 864e5 * 5 },
  { content: "\u4E0D\u592A\u559C\u6B22\u793E\u4EA4\u573A\u5408\uFF0C\u805A\u4F1A\u8D85\u8FC7\u5341\u4E2A\u4EBA\u5C31\u4E0D\u81EA\u5728", scope: "preference", ts: Date.now() - 864e5 * 120, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 864e5 * 15 },
  { content: "\u505A\u4E8B\u559C\u6B22\u5217\u6E05\u5355\uFF0C\u6BCF\u5929\u7528\u6EF4\u7B54\u6E05\u5355\u7BA1\u7406\u4EFB\u52A1", scope: "fact", ts: Date.now() - 864e5 * 45, confidence: 0.83, recallCount: 3, lastAccessed: Date.now() - 864e5 * 2 },
  { content: "\u538B\u529B\u5927\u7684\u65F6\u5019\u559C\u6B22\u4E00\u4E2A\u4EBA\u53BB\u6C5F\u8FB9\u8D70\u8D70", scope: "fact", ts: Date.now() - 864e5 * 60, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 864e5 * 8 },
  { content: "2022 \u5E74\u4ECE\u4E0A\u6D77\u642C\u5230\u4E86\u5317\u4EAC\uFF0C\u56E0\u4E3A\u5B57\u8282\u7684 offer", scope: "episode", ts: Date.now() - 864e5 * 250, confidence: 0.9, recallCount: 3, lastAccessed: Date.now() - 864e5 * 20 },
  { content: "\u5728\u4E0A\u6D77\u7684\u65F6\u5019\u4F4F\u5728\u6D66\u4E1C\u5F20\u6C5F\uFF0C\u79BB\u516C\u53F8\u5F88\u8FD1", scope: "fact", ts: Date.now() - 864e5 * 280, confidence: 0.83, recallCount: 1, lastAccessed: Date.now() - 864e5 * 30 },
  { content: "\u53BB\u5E74\u56FD\u5E86\u53BB\u4E86\u897F\u5B89\uFF0C\u770B\u4E86\u5175\u9A6C\u4FD1\u548C\u5927\u5510\u4E0D\u591C\u57CE", scope: "episode", ts: Date.now() - 864e5 * 160, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 864e5 * 25 },
  { content: "\u871C\u6708\u8BA1\u5212\u53BB\u9A6C\u5C14\u4EE3\u592B\uFF0C\u5DF2\u7ECF\u5728\u770B\u653B\u7565\u4E86", scope: "fact", ts: Date.now() - 864e5 * 6, confidence: 0.8, recallCount: 1, lastAccessed: Date.now() - 864e5 * 1 },
  { content: "\u5927\u5B66\u7684\u65F6\u5019\u4E00\u4E2A\u4EBA\u80CC\u5305\u53BB\u4E86\u4E91\u5357\uFF0C\u4F4F\u4E86\u534A\u4E2A\u6708", scope: "episode", ts: Date.now() - 864e5 * 300, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 864e5 * 40 },
  { content: "\u51FA\u5DEE\u53BB\u8FC7\u6DF1\u5733\u3001\u5E7F\u5DDE\u3001\u6210\u90FD\uFF0C\u6700\u559C\u6B22\u6210\u90FD", scope: "fact", ts: Date.now() - 864e5 * 100, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 864e5 * 20 },
  { content: "\u6709\u9009\u62E9\u56F0\u96BE\u75C7\uFF0C\u70B9\u5916\u5356\u80FD\u7EA0\u7ED3\u5341\u5206\u949F", scope: "fact", ts: Date.now() - 864e5 * 50, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - 864e5 * 5 },
  { content: "\u6211\u4E60\u60EF\u628A\u624B\u673A\u8C03\u6210\u9759\u97F3\uFF0C\u7ECF\u5E38\u6F0F\u63A5\u7535\u8BDD", scope: "fact", ts: Date.now() - 864e5 * 35, confidence: 0.78, recallCount: 2, lastAccessed: Date.now() - 864e5 * 3 },
  { content: "\u4E0D\u559C\u6B22\u9EBB\u70E6\u522B\u4EBA\uFF0C\u80FD\u81EA\u5DF1\u641E\u5B9A\u7684\u7EDD\u4E0D\u6C42\u4EBA", scope: "preference", ts: Date.now() - 864e5 * 110, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 864e5 * 10 },
  { content: "\u60C5\u7EEA\u4E0D\u597D\u7684\u65F6\u5019\u4F1A\u66B4\u996E\u66B4\u98DF", scope: "fact", ts: Date.now() - 864e5 * 70, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - 864e5 * 8 },
  { content: "\u524D\u5E74\u5B66\u4E86\u6F5C\u6C34\uFF0C\u8003\u4E86 PADI OW \u8BC1", scope: "fact", ts: Date.now() - 864e5 * 200, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 864e5 * 25 },
  { content: "\u4ECA\u5E74\u751F\u65E5\u6536\u5230\u4E86\u4E00\u5757\u5C0F\u96E8\u9001\u7684 Apple Watch", scope: "episode", ts: Date.now() - 864e5 * 40, confidence: 0.83, recallCount: 2, lastAccessed: Date.now() - 864e5 * 5 },
  { content: "\u548C\u524D\u5973\u53CB\u5206\u624B\u662F\u56E0\u4E3A\u5F02\u5730\u604B\u6491\u4E0D\u4E0B\u53BB\u4E86", scope: "fact", ts: Date.now() - 864e5 * 350, confidence: 0.82, recallCount: 1, lastAccessed: Date.now() - 864e5 * 50 },
  { content: "\u7B2C\u4E00\u4EFD\u5DE5\u4F5C\u662F\u5728\u7F8E\u56E2\u5B9E\u4E60\u8F6C\u6B63\u7684", scope: "fact", ts: Date.now() - 864e5 * 290, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 864e5 * 35 },
  // ── 180-199: More specific details ──
  { content: "\u624B\u673A\u7528\u7684\u662F iPhone 15 Pro Max\uFF0C\u4E4B\u524D\u4E00\u76F4\u7528\u5B89\u5353", scope: "fact", ts: Date.now() - 864e5 * 30, confidence: 0.85, recallCount: 2, lastAccessed: Date.now() - 864e5 * 3 },
  { content: '\u6700\u8BA8\u538C\u88AB\u95EE"\u4F60\u4EC0\u4E48\u65F6\u5019\u7ED3\u5A5A"', scope: "preference", ts: Date.now() - 864e5 * 40, confidence: 0.82, recallCount: 3, lastAccessed: Date.now() - 864e5 * 5 },
  { content: "\u6211\u7528 Spotify \u542C\u6B4C\uFF0C\u4E0D\u7528\u7F51\u6613\u4E91\u56E0\u4E3A\u7248\u6743\u5C11", scope: "preference", ts: Date.now() - 864e5 * 25, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - 864e5 * 3 },
  { content: "\u559C\u6B22\u559D\u7F8E\u5F0F\u5496\u5561\uFF0C\u4E0D\u52A0\u7CD6\u4E0D\u52A0\u5976", scope: "preference", ts: Date.now() - 864e5 * 50, confidence: 0.88, recallCount: 4, lastAccessed: Date.now() - 864e5 * 1 },
  { content: "\u6709\u4E00\u526F AirPods Pro\uFF0C\u901A\u52E4\u65F6\u6234\u7740\u542C\u64AD\u5BA2", scope: "fact", ts: Date.now() - 864e5 * 35, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 864e5 * 2 },
  { content: "\u6700\u8FD1\u5728\u542C\u4E00\u4E2A\u53EB\u300A\u786C\u5730\u9A87\u5BA2\u300B\u7684\u6280\u672F\u64AD\u5BA2", scope: "fact", ts: Date.now() - 864e5 * 10, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - 864e5 * 2 },
  { content: "\u6BCF\u5E74 618 \u548C\u53CC\u5341\u4E00\u4F1A\u5C6F\u4E00\u6279\u4E66", scope: "fact", ts: Date.now() - 864e5 * 45, confidence: 0.8, recallCount: 1, lastAccessed: Date.now() - 864e5 * 10 },
  { content: "\u6700\u8FD1\u60F3\u5B66\u6444\u5F71\uFF0C\u770B\u4E2D\u4E86\u4E00\u53F0\u5BCC\u58EB X-T5", scope: "fact", ts: Date.now() - 864e5 * 4, confidence: 0.78, recallCount: 1, lastAccessed: Date.now() - 864e5 * 1 },
  { content: "\u4E0A\u6B21\u642C\u5BB6\u6254\u4E86\u5341\u51E0\u7BB1\u65E7\u4E66\u548C\u8863\u670D", scope: "episode", ts: Date.now() - 864e5 * 250, confidence: 0.8, recallCount: 1, lastAccessed: Date.now() - 864e5 * 30 },
  { content: "\u6211\u6709\u4E00\u53CC Nike \u8DD1\u978B\u548C\u4E00\u53CC Adidas \u7BEE\u7403\u978B", scope: "fact", ts: Date.now() - 864e5 * 55, confidence: 0.78, recallCount: 1, lastAccessed: Date.now() - 864e5 * 8 },
  { content: "\u7761\u89C9\u5FC5\u987B\u5F00\u7A7A\u8C03\uFF0C\u4E0D\u7BA1\u51AC\u5929\u590F\u5929", scope: "fact", ts: Date.now() - 864e5 * 60, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 864e5 * 3 },
  { content: "\u7528 Chrome \u6D4F\u89C8\u5668\uFF0C\u88C5\u4E86\u5341\u51E0\u4E2A\u6269\u5C55", scope: "fact", ts: Date.now() - 864e5 * 40, confidence: 0.78, recallCount: 1, lastAccessed: Date.now() - 864e5 * 5 },
  { content: "\u6709\u5F3A\u8FEB\u75C7\u503E\u5411\uFF0C\u51FA\u95E8\u603B\u662F\u53CD\u590D\u786E\u8BA4\u9501\u6CA1\u9501\u95E8", scope: "fact", ts: Date.now() - 864e5 * 75, confidence: 0.83, recallCount: 2, lastAccessed: Date.now() - 864e5 * 6 },
  { content: "\u505A\u83DC\u559C\u6B22\u653E\u5F88\u591A\u849C\uFF0C\u5C0F\u96E8\u5ACC\u5473\u9053\u5927", scope: "fact", ts: Date.now() - 864e5 * 30, confidence: 0.8, recallCount: 2, lastAccessed: Date.now() - 864e5 * 4 },
  { content: "\u6BCF\u5468\u548C\u7238\u5988\u89C6\u9891\u901A\u8BDD\u4E24\u6B21\uFF0C\u4E00\u822C\u5468\u4E09\u548C\u5468\u65E5", scope: "fact", ts: Date.now() - 864e5 * 20, confidence: 0.85, recallCount: 3, lastAccessed: Date.now() - 864e5 * 2 },
  { content: "\u516C\u53F8\u6709\u4E2A\u8BFB\u4E66\u4F1A\uFF0C\u6211\u63A8\u8350\u4E86\u300A\u9ED1\u5BA2\u4E0E\u753B\u5BB6\u300B", scope: "fact", ts: Date.now() - 864e5 * 18, confidence: 0.8, recallCount: 1, lastAccessed: Date.now() - 864e5 * 5 },
  { content: "\u590F\u5929\u559C\u6B22\u7A7F\u62D6\u978B\u77ED\u88E4\uFF0C\u51AC\u5929\u5168\u9760\u7FBD\u7ED2\u670D", scope: "fact", ts: Date.now() - 864e5 * 100, confidence: 0.78, recallCount: 1, lastAccessed: Date.now() - 864e5 * 20 },
  { content: "\u53E3\u8154\u6E83\u75A1\u53CD\u590D\u53D1\u4F5C\uFF0C\u533B\u751F\u8BF4\u7F3A\u7EF4\u751F\u7D20 B", scope: "fact", ts: Date.now() - 864e5 * 15, confidence: 0.82, recallCount: 2, lastAccessed: Date.now() - 864e5 * 4 },
  { content: "\u6700\u8FD1\u5728\u7814\u7A76 Home Assistant \u641E\u667A\u80FD\u5BB6\u5C45", scope: "fact", ts: Date.now() - 864e5 * 7, confidence: 0.8, recallCount: 1, lastAccessed: Date.now() - 864e5 * 1 },
  { content: "\u5468\u672B\u5076\u5C14\u548C\u5C0F\u96E8\u4E00\u8D77\u53BB\u5B9C\u5BB6\u901B\u8857", scope: "fact", ts: Date.now() - 864e5 * 22, confidence: 0.78, recallCount: 2, lastAccessed: Date.now() - 864e5 * 4 }
];
const TEST_CASES = [
  // ════════════════════════════════════════════════════════════
  // DIRECT QUERIES (100 total)
  // ════════════════════════════════════════════════════════════
  // Memory 0-19: Original direct
  { query: "\u4F60\u5728\u54EA\u91CC\u4E0A\u73ED", expectedIndex: 0, type: "direct", description: "\u5DE5\u4F5C\u2192\u5B57\u8282" },
  { query: "\u4F60\u5973\u670B\u53CB\u53EB\u4EC0\u4E48", expectedIndex: 1, type: "direct", description: "\u5973\u670B\u53CB\u2192\u5C0F\u96E8" },
  { query: "\u4F60\u8840\u538B\u600E\u4E48\u6837", expectedIndex: 2, type: "direct", description: "\u8840\u538B\u2192\u9AD8" },
  { query: "\u4F60\u517B\u4E86\u4EC0\u4E48\u5BA0\u7269", expectedIndex: 3, type: "direct", description: "\u5BA0\u7269\u2192\u6A58\u732B" },
  { query: "\u4F60\u5728\u54EA\u91CC\u4E0A\u7684\u5927\u5B66", expectedIndex: 4, type: "direct", description: "\u5927\u5B66\u2192\u6B66\u6C49" },
  { query: "\u4F60\u53BB\u8FC7\u6210\u90FD\u5417", expectedIndex: 5, type: "direct", description: "\u6210\u90FD\u2192\u65C5\u6E38" },
  { query: "\u4F60\u6BCF\u5929\u8DD1\u591A\u5C11\u516C\u91CC", expectedIndex: 6, type: "direct", description: "\u8DD1\u6B65\u21925\u516C\u91CC" },
  { query: "\u4F60\u5728\u5B66\u4EC0\u4E48\u65B0\u6280\u672F", expectedIndex: 7, type: "direct", description: "\u6280\u672F\u2192Rust" },
  { query: "\u4F60\u5988\u505A\u4EC0\u4E48\u83DC\u597D\u5403", expectedIndex: 8, type: "direct", description: "\u5988\u2192\u7EA2\u70E7\u8089" },
  { query: "\u4F60\u9762\u8BD5\u963F\u91CC\u600E\u4E48\u6837\u4E86", expectedIndex: 9, type: "direct", description: "\u9762\u8BD5\u2192\u963F\u91CC" },
  { query: "\u4F60\u7761\u7720\u600E\u4E48\u6837", expectedIndex: 10, type: "direct", description: "\u7761\u7720\u2192\u5931\u7720" },
  { query: "\u4F60\u6BCF\u4E2A\u6708\u8FD8\u591A\u5C11\u623F\u8D37", expectedIndex: 11, type: "direct", description: "\u623F\u8D37\u21928000" },
  { query: "\u5C0F\u96E8\u9884\u4EA7\u671F\u662F\u4EC0\u4E48\u65F6\u5019", expectedIndex: 12, type: "direct", description: "\u9884\u4EA7\u671F\u2192\u4E09\u6708" },
  { query: "\u4F60\u559C\u6B22\u770B\u4EC0\u4E48\u7535\u5F71", expectedIndex: 13, type: "direct", description: "\u7535\u5F71\u2192\u79D1\u5E7B" },
  { query: "\u4F60\u5468\u672B\u6253\u7BEE\u7403\u5417", expectedIndex: 14, type: "direct", description: "\u7BEE\u7403\u2192\u5468\u672B" },
  { query: "\u4F60\u5BF9\u4EC0\u4E48\u8FC7\u654F", expectedIndex: 15, type: "direct", description: "\u8FC7\u654F\u2192\u82B1\u7C89" },
  { query: "\u4F60\u60F3\u4E70\u4EC0\u4E48\u8F66", expectedIndex: 16, type: "direct", description: "\u4E70\u8F66\u2192\u7279\u65AF\u62C9" },
  { query: "\u4F60\u8001\u5BB6\u5728\u54EA\u91CC", expectedIndex: 17, type: "direct", description: "\u8001\u5BB6\u2192\u957F\u6C99" },
  { query: "\u4F60\u4E0B\u4E2A\u6708\u6709\u4EC0\u4E48\u5B89\u6392", expectedIndex: 18, type: "direct", description: "\u5B89\u6392\u2192\u5A5A\u793C" },
  { query: "\u4F60\u6700\u8FD1\u52A0\u73ED\u591A\u5417", expectedIndex: 19, type: "direct", description: "\u52A0\u73ED\u2192\u5341\u4E00\u70B9" },
  // Memory 20-39: Second batch direct
  { query: "\u6211\u51E0\u70B9\u8D77\u5E8A", expectedIndex: 20, type: "direct", description: "\u8D77\u5E8A\u21927\u70B9\u8DD1\u6B65" },
  { query: "\u6211\u5BF9\u4EC0\u4E48\u8FC7\u654F", expectedIndex: 21, type: "direct", description: "\u8FC7\u654F\u2192\u82B1\u7C89" },
  { query: "\u6211\u5F00\u4EC0\u4E48\u8F66", expectedIndex: 22, type: "direct", description: "\u5F00\u8F66\u2192\u7279\u65AF\u62C9" },
  { query: "\u6211\u5DE5\u8D44\u6DA8\u4E86\u591A\u5C11", expectedIndex: 23, type: "direct", description: "\u6DA8\u85AA\u21922000" },
  { query: "\u6211\u5973\u513F\u5B66\u4EC0\u4E48\u4E50\u5668", expectedIndex: 24, type: "direct", description: "\u4E50\u5668\u2192\u94A2\u7434" },
  { query: "\u6211\u6212\u70DF\u591A\u4E45\u4E86", expectedIndex: 25, type: "direct", description: "\u6212\u70DF\u219247\u5929" },
  { query: "\u6211\u6015\u4EC0\u4E48", expectedIndex: 26, type: "direct", description: "\u6015\u2192\u86C7" },
  { query: "\u6211\u4E0B\u4E2A\u6708\u53BB\u54EA\u65C5\u6E38", expectedIndex: 27, type: "direct", description: "\u65C5\u6E38\u2192\u65E5\u672C" },
  { query: "\u6211\u5BA4\u53CB\u53EB\u4EC0\u4E48", expectedIndex: 28, type: "direct", description: "\u5BA4\u53CB\u2192\u5F20\u78CA" },
  { query: "\u6211\u4EC0\u4E48\u8840\u578B", expectedIndex: 29, type: "direct", description: "\u8840\u578B\u2192O\u578B" },
  { query: "\u5468\u672B\u4E00\u822C\u5E72\u561B", expectedIndex: 30, type: "direct", description: "\u5468\u672B\u2192\u966A\u5B69\u5B50\u516C\u56ED" },
  { query: "\u6211\u60F3\u53BB\u54EA\u4E2A\u516C\u53F8", expectedIndex: 31, type: "direct", description: "\u516C\u53F8\u2192\u963F\u91CC" },
  { query: "\u6211\u7092\u80A1\u4E8F\u4E86\u591A\u5C11", expectedIndex: 32, type: "direct", description: "\u7092\u80A1\u21923\u4E07" },
  { query: "\u6211\u5728\u5B66\u4EC0\u4E48\u8BED\u8A00", expectedIndex: 33, type: "direct", description: "\u5B66\u8BED\u8A00\u2192\u65E5\u8BED" },
  { query: "\u6211\u8001\u5A46\u600E\u4E48\u8BA4\u8BC6\u7684", expectedIndex: 34, type: "direct", description: "\u8001\u5A46\u2192\u5927\u5B66\u540C\u5B66" },
  { query: "\u6211\u7535\u8111\u4EC0\u4E48\u914D\u7F6E", expectedIndex: 35, type: "direct", description: "\u7535\u8111\u2192M2 Pro" },
  { query: "\u6211\u5468\u4E94\u505A\u4EC0\u4E48\u8FD0\u52A8", expectedIndex: 36, type: "direct", description: "\u5468\u4E94\u8FD0\u52A8\u2192\u7FBD\u6BDB\u7403" },
  { query: "\u6211\u6700\u8FD1\u5728\u770B\u4EC0\u4E48\u4E66", expectedIndex: 37, type: "direct", description: "\u770B\u4E66\u2192\u4E09\u4F53" },
  { query: "\u6211\u505A\u8FC7\u4EC0\u4E48\u624B\u672F", expectedIndex: 38, type: "direct", description: "\u624B\u672F\u2192\u8FD1\u89C6" },
  { query: "\u6211\u5728\u54EA\u5DE5\u4F5C", expectedIndex: 39, type: "direct", description: "\u5DE5\u4F5C\u2192\u5B57\u8282\u5B89\u5168" },
  // Memory 40-43: Social media direct
  { query: "\u6211\u6BCF\u5929\u5237\u6296\u97F3\u591A\u4E45", expectedIndex: 40, type: "direct", description: "\u6296\u97F3\u2192\u4E24\u5C0F\u65F6" },
  { query: "\u6211\u6709\u6280\u672F\u535A\u5BA2\u5417", expectedIndex: 41, type: "direct", description: "\u535A\u5BA2\u219250\u7BC7" },
  { query: "\u6211\u5FAE\u4FE1\u6709\u591A\u5C11\u597D\u53CB", expectedIndex: 42, type: "direct", description: "\u5FAE\u4FE1\u21922000\u4EBA" },
  { query: "\u6211\u5728\u5C0F\u7EA2\u4E66\u4E0A\u5173\u6CE8\u4EC0\u4E48", expectedIndex: 43, type: "direct", description: "\u5C0F\u7EA2\u4E66\u2192\u7F8E\u98DF\u535A\u4E3B" },
  // Memory 44-47: Music direct
  { query: "\u6211\u6700\u559C\u6B22\u8C01\u7684\u6B4C", expectedIndex: 44, type: "direct", description: "\u559C\u6B22\u6B4C\u2192\u5468\u6770\u4F26" },
  { query: "\u5199\u4EE3\u7801\u65F6\u542C\u4EC0\u4E48\u97F3\u4E50", expectedIndex: 45, type: "direct", description: "\u4EE3\u7801\u97F3\u4E50\u2192lo-fi" },
  { query: "\u6211\u53BB\u770B\u8FC7\u4EC0\u4E48\u6F14\u5531\u4F1A", expectedIndex: 46, type: "direct", description: "\u6F14\u5531\u4F1A\u2192\u4E94\u6708\u5929" },
  { query: "\u6211\u5C0F\u65F6\u5019\u5B66\u8FC7\u4EC0\u4E48\u4E50\u5668", expectedIndex: 47, type: "direct", description: "\u4E50\u5668\u2192\u5C0F\u63D0\u7434" },
  // Memory 48-51: Cooking direct
  { query: "\u6211\u7684\u62FF\u624B\u83DC\u662F\u4EC0\u4E48", expectedIndex: 48, type: "direct", description: "\u62FF\u624B\u83DC\u2192\u7CD6\u918B\u6392\u9AA8" },
  { query: "\u6211\u7528\u4EC0\u4E48 App \u770B\u83DC\u8C31", expectedIndex: 49, type: "direct", description: "\u83DC\u8C31\u2192\u4E0B\u53A8\u623F" },
  { query: "\u6211\u6700\u8FD1\u5B66\u4F1A\u505A\u4EC0\u4E48\u751C\u54C1", expectedIndex: 50, type: "direct", description: "\u751C\u54C1\u2192\u63D0\u62C9\u7C73\u82CF" },
  { query: "\u6211\u4E0D\u5403\u4EC0\u4E48\u83DC", expectedIndex: 51, type: "direct", description: "\u4E0D\u5403\u2192\u9999\u83DC" },
  // Memory 52-55: Weather direct
  { query: "\u4F60\u6015\u51B7\u5417", expectedIndex: 52, type: "direct", description: "\u6015\u51B7\u2192\u51AC\u5929\u4E0D\u51FA\u95E8" },
  { query: "\u4F60\u6700\u559C\u6B22\u4EC0\u4E48\u5B63\u8282", expectedIndex: 53, type: "direct", description: "\u5B63\u8282\u2192\u79CB\u5929" },
  { query: "\u4E0B\u96E8\u5929\u4F60\u4E00\u822C\u5E72\u561B", expectedIndex: 54, type: "direct", description: "\u4E0B\u96E8\u2192\u6253\u6E38\u620F" },
  { query: "\u4F60\u4E2D\u6691\u8FC7\u5417", expectedIndex: 55, type: "direct", description: "\u4E2D\u6691\u2192\u516C\u53F8\u6655\u5012" },
  // Memory 56-59: Childhood direct
  { query: "\u4F60\u5C0F\u65F6\u5019\u5728\u54EA\u91CC\u957F\u5927", expectedIndex: 56, type: "direct", description: "\u5C0F\u65F6\u5019\u2192\u519C\u6751" },
  { query: "\u4F60\u6570\u5B66\u6210\u7EE9\u597D\u5417", expectedIndex: 57, type: "direct", description: "\u6570\u5B66\u2192\u7ADE\u8D5B\u4E00\u7B49\u5956" },
  { query: "\u4F60\u6015\u6253\u9488\u5417", expectedIndex: 58, type: "direct", description: "\u6253\u9488\u2192\u6015" },
  { query: "\u4F60\u5C0F\u65F6\u5019\u517B\u8FC7\u4EC0\u4E48\u52A8\u7269", expectedIndex: 59, type: "direct", description: "\u52A8\u7269\u2192\u72D7\u65FA\u8D22" },
  // Memory 60-63: Goals direct
  { query: "\u4F60\u7684\u68A6\u60F3\u662F\u4EC0\u4E48", expectedIndex: 60, type: "direct", description: "\u68A6\u60F3\u2192\u5496\u5561\u5E97" },
  { query: "\u4F60\u6253\u7B97\u8003\u4EC0\u4E48\u8BC1", expectedIndex: 61, type: "direct", description: "\u8003\u8BC1\u2192PMP" },
  { query: "\u4F60\u60F3\u6512\u591A\u5C11\u94B1", expectedIndex: 62, type: "direct", description: "\u6512\u94B1\u2192200\u4E07" },
  { query: "\u4F60\u7ED9\u7236\u6BCD\u6709\u4EC0\u4E48\u6253\u7B97", expectedIndex: 63, type: "direct", description: "\u7236\u6BCD\u2192\u76D6\u623F\u5B50" },
  // Memory 64-67: Routines direct
  { query: "\u4F60\u65E9\u4E0A\u5148\u5E72\u561B", expectedIndex: 64, type: "direct", description: "\u65E9\u4E0A\u2192\u559D\u5496\u5561" },
  { query: "\u4F60\u4E2D\u5348\u5728\u54EA\u5403\u996D", expectedIndex: 65, type: "direct", description: "\u4E2D\u5348\u2192\u98DF\u5802" },
  { query: "\u4F60\u665A\u4E0A\u6D17\u5B8C\u6FA1\u5E72\u561B", expectedIndex: 66, type: "direct", description: "\u6D17\u6FA1\u540E\u2192B\u7AD9" },
  { query: "\u4F60\u7761\u524D\u505A\u4EC0\u4E48", expectedIndex: 67, type: "direct", description: "\u7761\u524D\u2192\u5237\u5FAE\u535A" },
  // Memory 68-71: Shopping direct
  { query: "\u4F60\u6BCF\u4E2A\u6708\u7F51\u8D2D\u82B1\u591A\u5C11\u94B1", expectedIndex: 68, type: "direct", description: "\u7F51\u8D2D\u21923000" },
  { query: "\u4F60\u53CC\u5341\u4E00\u4E70\u4E86\u4EC0\u4E48", expectedIndex: 69, type: "direct", description: "\u53CC\u5341\u4E00\u2192\u96F6\u98DF\u65E5\u7528\u54C1" },
  { query: "\u4F60\u5728\u54EA\u4E70\u8863\u670D", expectedIndex: 70, type: "direct", description: "\u4E70\u8863\u670D\u2192\u4F18\u8863\u5E93Zara" },
  { query: "\u4F60\u4E70\u76F2\u76D2\u82B1\u4E86\u591A\u5C11", expectedIndex: 71, type: "direct", description: "\u76F2\u76D2\u2192\u4E00\u5343\u591A" },
  // Memory 72-75: Transport direct
  { query: "\u4F60\u600E\u4E48\u4E0A\u73ED", expectedIndex: 72, type: "direct", description: "\u4E0A\u73ED\u2192\u5730\u94C12\u8F6C10" },
  { query: "\u4F60\u4E0A\u73ED\u8DEF\u4E0A\u8981\u591A\u4E45", expectedIndex: 73, type: "direct", description: "\u901A\u52E4\u2192\u4E00\u4E2A\u534A\u5C0F\u65F6" },
  { query: "\u4F60\u9A91\u5171\u4EAB\u5355\u8F66\u5417", expectedIndex: 74, type: "direct", description: "\u5355\u8F66\u2192\u53BB\u5730\u94C1\u7AD9" },
  { query: "\u4F60\u6709\u9A7E\u7167\u5417", expectedIndex: 75, type: "direct", description: "\u9A7E\u7167\u2192\u6709\u4F46\u4E0D\u6562\u5F00" },
  // Memory 76-79: News direct
  { query: "\u4F60\u770B\u4EC0\u4E48\u65B0\u95FB", expectedIndex: 76, type: "direct", description: "\u65B0\u95FB\u219236kr\u79D1\u6280" },
  { query: "\u4F60\u5173\u6CE8 AI \u5417", expectedIndex: 77, type: "direct", description: "AI\u2192\u5927\u6A21\u578B" },
  { query: "\u4F60\u770B\u5A31\u4E50\u516B\u5366\u5417", expectedIndex: 78, type: "direct", description: "\u516B\u5366\u2192\u4E0D\u770B" },
  { query: "\u4F60\u5728 B \u7AD9\u5173\u6CE8\u4E86\u8C01", expectedIndex: 79, type: "direct", description: "B\u7AD9\u2192\u534A\u4F5B\u4ED9\u4EBA" },
  // ════════════════════════════════════════════════════════════
  // SEMANTIC QUERIES (100 total)
  // ════════════════════════════════════════════════════════════
  // Memory 0-19: Original semantic
  { query: "\u4F60\u4F1A\u4EC0\u4E48\u7F16\u7A0B\u8BED\u8A00", expectedIndex: 0, type: "semantic", description: "\u7F16\u7A0B\u8BED\u8A00\u2192Go" },
  { query: "\u4F60\u5BF9\u8C61\u662F\u8C01", expectedIndex: 1, type: "semantic", description: "\u5BF9\u8C61\u2192\u5973\u670B\u53CB" },
  { query: "\u4F60\u6709\u4EC0\u4E48\u5065\u5EB7\u95EE\u9898", expectedIndex: 2, type: "semantic", description: "\u5065\u5EB7\u2192\u8840\u538B" },
  { query: "\u6A58\u5B50\u6700\u8FD1\u600E\u4E48\u6837", expectedIndex: 3, type: "semantic", description: "\u6A58\u5B50\u2192\u732B\u540D" },
  { query: "\u4F60\u6BCD\u6821\u5728\u54EA", expectedIndex: 4, type: "semantic", description: "\u6BCD\u6821\u2192\u5927\u5B66" },
  { query: "\u4F60\u559C\u6B22\u5403\u4EC0\u4E48\u7F8E\u98DF", expectedIndex: 5, type: "semantic", description: "\u7F8E\u98DF\u2192\u706B\u9505" },
  { query: "\u4F60\u6709\u4EC0\u4E48\u953B\u70BC\u4E60\u60EF", expectedIndex: 6, type: "semantic", description: "\u953B\u70BC\u2192\u8DD1\u6B65" },
  { query: "\u6240\u6709\u6743\u7CFB\u7EDF\u4F60\u641E\u61C2\u4E86\u5417", expectedIndex: 7, type: "semantic", description: "\u6240\u6709\u6743\u2192Rust" },
  { query: "\u4F60\u56DE\u5BB6\u6700\u60F3\u5403\u4EC0\u4E48", expectedIndex: 8, type: "semantic", description: "\u56DE\u5BB6\u5403\u2192\u7EA2\u70E7\u8089" },
  { query: "\u4F60\u6700\u8FD1\u6709\u6CA1\u6709\u627E\u5DE5\u4F5C", expectedIndex: 9, type: "semantic", description: "\u627E\u5DE5\u4F5C\u2192\u9762\u8BD5" },
  { query: "\u4F60\u51E0\u70B9\u7761\u89C9", expectedIndex: 10, type: "semantic", description: "\u51E0\u70B9\u7761\u2192\u51CC\u6668\u4E00\u70B9" },
  { query: "\u4F60\u6709\u4EC0\u4E48\u7ECF\u6D4E\u538B\u529B", expectedIndex: 11, type: "semantic", description: "\u7ECF\u6D4E\u538B\u529B\u2192\u623F\u8D37" },
  { query: "\u4F60\u8981\u5F53\u7238\u7238\u4E86\u5417", expectedIndex: 12, type: "semantic", description: "\u5F53\u7238\u7238\u2192\u6000\u5B55" },
  { query: "\u661F\u9645\u7A7F\u8D8A\u4F60\u770B\u8FC7\u5417", expectedIndex: 13, type: "semantic", description: "\u661F\u9645\u7A7F\u8D8A\u2192\u6700\u559C\u6B22" },
  { query: "\u4F60\u6709\u4EC0\u4E48\u8FD0\u52A8\u7231\u597D", expectedIndex: 14, type: "semantic", description: "\u8FD0\u52A8\u7231\u597D\u2192\u7BEE\u7403" },
  { query: "\u6625\u5929\u51FA\u95E8\u4F60\u8981\u6CE8\u610F\u4EC0\u4E48", expectedIndex: 15, type: "semantic", description: "\u6625\u5929\u6CE8\u610F\u2192\u53E3\u7F69" },
  { query: "\u4F60\u8003\u8651\u5165\u624B\u7535\u52A8\u8F66\u5417", expectedIndex: 16, type: "semantic", description: "\u7535\u52A8\u8F66\u2192\u7279\u65AF\u62C9" },
  { query: "\u4F60\u80FD\u5403\u8FA3\u5417", expectedIndex: 17, type: "semantic", description: "\u5403\u8FA3\u2192\u6E56\u5357" },
  { query: "\u4EFD\u5B50\u94B1\u51C6\u5907\u4E86\u591A\u5C11", expectedIndex: 18, type: "semantic", description: "\u4EFD\u5B50\u94B1\u2192\u5A5A\u793C" },
  { query: "\u4F60\u5DE5\u4F5C\u7D2F\u4E0D\u7D2F", expectedIndex: 19, type: "semantic", description: "\u5DE5\u4F5C\u7D2F\u2192\u52A0\u73ED" },
  // Memory 20-39: Second batch semantic
  { query: "\u6211\u7684\u6668\u7EC3\u4E60\u60EF", expectedIndex: 20, type: "semantic", description: "\u6668\u7EC3\u2192\u8DD1\u6B65" },
  { query: "\u6211\u6709\u4EC0\u4E48\u5065\u5EB7\u9690\u60A3", expectedIndex: [21, 38], type: "semantic", description: "\u5065\u5EB7\u9690\u60A3\u2192\u8FC7\u654F/\u8FD1\u89C6" },
  { query: "\u6211\u7684\u4EA4\u901A\u5DE5\u5177", expectedIndex: 22, type: "semantic", description: "\u4EA4\u901A\u5DE5\u5177\u2192\u7279\u65AF\u62C9" },
  { query: "\u6211\u7684\u6536\u5165\u53D8\u5316", expectedIndex: 23, type: "semantic", description: "\u6536\u5165\u53D8\u5316\u2192\u6DA8\u85AA" },
  { query: "\u5B69\u5B50\u7684\u8BFE\u5916\u6D3B\u52A8", expectedIndex: 24, type: "semantic", description: "\u8BFE\u5916\u6D3B\u52A8\u2192\u94A2\u7434" },
  { query: "\u6211\u5728\u514B\u670D\u4EC0\u4E48\u574F\u4E60\u60EF", expectedIndex: 25, type: "semantic", description: "\u574F\u4E60\u60EF\u2192\u6212\u70DF" },
  { query: "\u6211\u7684\u6050\u60E7", expectedIndex: 26, type: "semantic", description: "\u6050\u60E7\u2192\u86C7" },
  { query: "\u6700\u8FD1\u7684\u65C5\u884C\u8BA1\u5212", expectedIndex: 27, type: "semantic", description: "\u65C5\u884C\u8BA1\u5212\u2192\u65E5\u672C" },
  { query: "\u6211\u7684\u8001\u540C\u5B66\u73B0\u5728\u5E72\u561B", expectedIndex: 28, type: "semantic", description: "\u8001\u540C\u5B66\u2192\u5F20\u78CA\u817E\u8BAF" },
  { query: "\u6211\u7684\u804C\u4E1A\u89C4\u5212", expectedIndex: 31, type: "semantic", description: "\u804C\u4E1A\u89C4\u5212\u2192\u6362\u5DE5\u4F5C\u963F\u91CC" },
  { query: "\u6211\u7684\u6295\u8D44\u60C5\u51B5", expectedIndex: 32, type: "semantic", description: "\u6295\u8D44\u2192\u7092\u80A1\u4E8F3\u4E07" },
  { query: "\u6211\u5728\u81EA\u6211\u63D0\u5347\u4EC0\u4E48", expectedIndex: 33, type: "semantic", description: "\u81EA\u6211\u63D0\u5347\u2192\u5B66\u65E5\u8BED" },
  { query: "\u6211\u548C\u8001\u5A46\u7684\u6545\u4E8B", expectedIndex: 34, type: "semantic", description: "\u8001\u5A46\u6545\u4E8B\u2192\u5927\u5B66\u540C\u5B66" },
  { query: "\u6211\u7684\u6570\u7801\u88C5\u5907", expectedIndex: 35, type: "semantic", description: "\u6570\u7801\u88C5\u5907\u2192MacBook" },
  { query: "\u6211\u7684\u8FD0\u52A8\u4E60\u60EF", expectedIndex: [20, 36], type: "semantic", description: "\u8FD0\u52A8\u2192\u8DD1\u6B65/\u7FBD\u6BDB\u7403" },
  { query: "\u6211\u7684\u9605\u8BFB\u504F\u597D", expectedIndex: 37, type: "semantic", description: "\u9605\u8BFB\u2192\u4E09\u4F53" },
  { query: "\u6211\u7684\u89C6\u529B\u60C5\u51B5", expectedIndex: 38, type: "semantic", description: "\u89C6\u529B\u2192\u8FD1\u89C6\u624B\u672F" },
  { query: "\u6211\u5BB6\u91CC\u51E0\u53E3\u4EBA", expectedIndex: [24, 34], type: "semantic", description: "\u5BB6\u4EBA\u2192\u8001\u5A46+\u5973\u513F" },
  { query: "\u6211\u5468\u672B\u7684\u5B89\u6392", expectedIndex: 30, type: "semantic", description: "\u5468\u672B\u5B89\u6392\u2192\u966A\u5B69\u5B50\u516C\u56ED" },
  { query: "\u6211\u6700\u8FD1\u6709\u4EC0\u4E48\u70E6\u5FC3\u4E8B", expectedIndex: [32, 31], type: "semantic", description: "\u70E6\u5FC3\u4E8B\u2192\u4E8F\u94B1/\u6362\u5DE5\u4F5C" },
  // Memory 40-43: Social media semantic
  { query: "\u4F60\u5E73\u65F6\u73A9\u4EC0\u4E48\u77ED\u89C6\u9891", expectedIndex: 40, type: "semantic", description: "\u77ED\u89C6\u9891\u2192\u6296\u97F3" },
  { query: "\u4F60\u6709\u6CA1\u6709\u5728\u7F51\u4E0A\u5199\u4E1C\u897F", expectedIndex: 41, type: "semantic", description: "\u5199\u4E1C\u897F\u2192\u6280\u672F\u535A\u5BA2" },
  { query: "\u4F60\u7684\u793E\u4EA4\u5708\u5927\u5417", expectedIndex: 42, type: "semantic", description: "\u793E\u4EA4\u5708\u2192\u5FAE\u4FE12000\u4EBA" },
  { query: "\u4F60\u5E73\u65F6\u600E\u4E48\u53D1\u73B0\u597D\u5403\u7684", expectedIndex: 43, type: "semantic", description: "\u53D1\u73B0\u7F8E\u98DF\u2192\u5C0F\u7EA2\u4E66" },
  // Memory 44-47: Music semantic
  { query: "\u4F60\u7684\u97F3\u4E50\u54C1\u5473", expectedIndex: 44, type: "semantic", description: "\u97F3\u4E50\u54C1\u5473\u2192\u5468\u6770\u4F26" },
  { query: "\u4F60\u5DE5\u4F5C\u65F6\u9700\u8981\u4EC0\u4E48\u6C1B\u56F4", expectedIndex: 45, type: "semantic", description: "\u5DE5\u4F5C\u6C1B\u56F4\u2192lo-fi\u97F3\u4E50" },
  { query: "\u4F60\u6700\u8FD1\u6709\u4EC0\u4E48\u5A31\u4E50\u6D3B\u52A8", expectedIndex: 46, type: "semantic", description: "\u5A31\u4E50\u6D3B\u52A8\u2192\u4E94\u6708\u5929\u6F14\u5531\u4F1A" },
  { query: "\u4F60\u6709\u4EC0\u4E48\u534A\u9014\u800C\u5E9F\u7684\u4E8B", expectedIndex: 47, type: "semantic", description: "\u534A\u9014\u800C\u5E9F\u2192\u5C0F\u63D0\u7434" },
  // Memory 48-51: Cooking semantic
  { query: "\u4F60\u53A8\u827A\u600E\u4E48\u6837", expectedIndex: 48, type: "semantic", description: "\u53A8\u827A\u2192\u7CD6\u918B\u6392\u9AA8" },
  { query: "\u4F60\u662F\u600E\u4E48\u5B66\u505A\u996D\u7684", expectedIndex: 49, type: "semantic", description: "\u5B66\u505A\u996D\u2192\u4E0B\u53A8\u623FApp" },
  { query: "\u4F60\u6700\u8FD1\u5728\u53A8\u623F\u641E\u4EC0\u4E48\u82B1\u6837", expectedIndex: 50, type: "semantic", description: "\u53A8\u623F\u82B1\u6837\u2192\u63D0\u62C9\u7C73\u82CF" },
  { query: "\u4F60\u6709\u4EC0\u4E48\u5FCC\u53E3", expectedIndex: 51, type: "semantic", description: "\u5FCC\u53E3\u2192\u9999\u83DC" },
  // Memory 52-55: Weather semantic
  { query: "\u4F60\u51AC\u5929\u4E00\u822C\u5B85\u5728\u5BB6\u5417", expectedIndex: 52, type: "semantic", description: "\u51AC\u5929\u5B85\u2192\u6015\u51B7" },
  { query: "\u4EC0\u4E48\u5929\u6C14\u8BA9\u4F60\u6700\u8212\u670D", expectedIndex: 53, type: "semantic", description: "\u8212\u670D\u5929\u6C14\u2192\u79CB\u5929" },
  { query: "\u4F60\u5E73\u65F6\u6253\u4EC0\u4E48\u6E38\u620F", expectedIndex: 54, type: "semantic", description: "\u6E38\u620F\u2192\u4E0B\u96E8\u5929" },
  { query: "\u4F60\u5728\u516C\u53F8\u51FA\u8FC7\u4EC0\u4E48\u72B6\u51B5", expectedIndex: 55, type: "semantic", description: "\u516C\u53F8\u72B6\u51B5\u2192\u4E2D\u6691\u6655\u5012" },
  // Memory 56-59: Childhood semantic
  { query: "\u4F60\u7684\u7AE5\u5E74\u662F\u4EC0\u4E48\u6837\u7684", expectedIndex: 56, type: "semantic", description: "\u7AE5\u5E74\u2192\u519C\u6751\u6478\u9C7C" },
  { query: "\u4F60\u4ECE\u5C0F\u5B66\u4E60\u5C31\u597D\u5417", expectedIndex: 57, type: "semantic", description: "\u5B66\u4E60\u597D\u2192\u6570\u5B66\u7ADE\u8D5B" },
  { query: "\u4F60\u53BB\u533B\u9662\u4F1A\u7D27\u5F20\u5417", expectedIndex: 58, type: "semantic", description: "\u533B\u9662\u7D27\u5F20\u2192\u6015\u6253\u9488" },
  { query: "\u4F60\u4EE5\u524D\u517B\u8FC7\u5BA0\u7269\u5417", expectedIndex: 59, type: "semantic", description: "\u4EE5\u524D\u5BA0\u7269\u2192\u65FA\u8D22" },
  // Memory 60-63: Goals semantic
  { query: "\u4F60\u6709\u4EC0\u4E48\u521B\u4E1A\u60F3\u6CD5", expectedIndex: 60, type: "semantic", description: "\u521B\u4E1A\u2192\u5496\u5561\u5E97" },
  { query: "\u4F60\u5728\u89C4\u5212\u4EC0\u4E48\u804C\u4E1A\u53D1\u5C55", expectedIndex: 61, type: "semantic", description: "\u804C\u4E1A\u53D1\u5C55\u2192PMP" },
  { query: "\u4F60\u7684\u8D22\u52A1\u76EE\u6807", expectedIndex: 62, type: "semantic", description: "\u8D22\u52A1\u76EE\u6807\u2192200\u4E07" },
  { query: "\u4F60\u5BF9\u7236\u6BCD\u7684\u5B5D\u5FC3", expectedIndex: 63, type: "semantic", description: "\u5B5D\u5FC3\u2192\u76D6\u623F" },
  // Memory 64-67: Routines semantic
  { query: "\u4F60\u6709\u4EC0\u4E48\u65E9\u8D77\u4EEA\u5F0F", expectedIndex: 64, type: "semantic", description: "\u65E9\u8D77\u4EEA\u5F0F\u2192\u5496\u5561" },
  { query: "\u4F60\u5348\u9910\u600E\u4E48\u89E3\u51B3", expectedIndex: 65, type: "semantic", description: "\u5348\u9910\u2192\u98DF\u5802" },
  { query: "\u4F60\u7684\u7761\u524D\u5A31\u4E50", expectedIndex: [66, 67], type: "semantic", description: "\u7761\u524D\u5A31\u4E50\u2192B\u7AD9/\u5FAE\u535A" },
  { query: "\u4F60\u6709\u4EC0\u4E48\u653E\u677E\u65B9\u5F0F", expectedIndex: [66, 54], type: "semantic", description: "\u653E\u677E\u2192B\u7AD9/\u6E38\u620F" },
  // Memory 68-71: Shopping semantic
  { query: "\u4F60\u6D88\u8D39\u6C34\u5E73\u600E\u4E48\u6837", expectedIndex: 68, type: "semantic", description: "\u6D88\u8D39\u6C34\u5E73\u2192\u7F51\u8D2D3000" },
  { query: "\u4F60\u56E4\u8D27\u4E25\u91CD\u5417", expectedIndex: 69, type: "semantic", description: "\u56E4\u8D27\u2192\u53CC\u5341\u4E00" },
  { query: "\u4F60\u7684\u7A7F\u8863\u98CE\u683C", expectedIndex: 70, type: "semantic", description: "\u7A7F\u8863\u2192\u4F18\u8863\u5E93Zara" },
  { query: "\u4F60\u6709\u4EC0\u4E48\u70E7\u94B1\u7684\u7231\u597D", expectedIndex: 71, type: "semantic", description: "\u70E7\u94B1\u7231\u597D\u2192\u76F2\u76D2" },
  // Memory 72-75: Transport semantic
  { query: "\u4F60\u7684\u901A\u52E4\u65B9\u5F0F", expectedIndex: 72, type: "semantic", description: "\u901A\u52E4\u2192\u5730\u94C1" },
  { query: "\u4F60\u6BCF\u5929\u82B1\u591A\u5C11\u65F6\u95F4\u5728\u8DEF\u4E0A", expectedIndex: 73, type: "semantic", description: "\u8DEF\u4E0A\u65F6\u95F4\u2192\u4E00\u4E2A\u534A\u5C0F\u65F6" },
  { query: "\u6700\u540E\u4E00\u516C\u91CC\u600E\u4E48\u89E3\u51B3", expectedIndex: 74, type: "semantic", description: "\u6700\u540E\u4E00\u516C\u91CC\u2192\u5171\u4EAB\u5355\u8F66" },
  { query: "\u4F60\u4F1A\u5F00\u8F66\u5417", expectedIndex: 75, type: "semantic", description: "\u5F00\u8F66\u2192\u6709\u9A7E\u7167\u4E0D\u6562\u5F00" },
  // Memory 76-79: News semantic
  { query: "\u4F60\u5173\u6CE8\u4EC0\u4E48\u9886\u57DF\u7684\u8D44\u8BAF", expectedIndex: 76, type: "semantic", description: "\u8D44\u8BAF\u2192\u79D1\u628036kr" },
  { query: "\u4F60\u5BF9 ChatGPT \u600E\u4E48\u770B", expectedIndex: 77, type: "semantic", description: "ChatGPT\u2192\u5173\u6CE8AI\u5927\u6A21\u578B" },
  { query: "\u4F60\u5BF9\u660E\u661F\u516B\u5366\u611F\u5174\u8DA3\u5417", expectedIndex: 78, type: "semantic", description: "\u660E\u661F\u516B\u5366\u2192\u4E0D\u770B" },
  { query: "\u4F60\u7528\u4EC0\u4E48\u6253\u53D1\u788E\u7247\u65F6\u95F4", expectedIndex: [79, 40], type: "semantic", description: "\u788E\u7247\u65F6\u95F4\u2192B\u7AD9/\u6296\u97F3" },
  // ════════════════════════════════════════════════════════════
  // CROSS-DOMAIN / MULTI-MATCH / HARD QUERIES (20 extra, filling to 200)
  // ════════════════════════════════════════════════════════════
  // Multi-memory: daily routine composite
  { query: "\u6211\u7684\u65E5\u5E38\u4F5C\u606F\u662F\u4EC0\u4E48\u6837\u7684", expectedIndex: [20, 64, 65, 66, 67], type: "semantic", description: "\u65E5\u5E38\u4F5C\u606F\u2192\u8D77\u5E8A+\u5496\u5561+\u98DF\u5802+B\u7AD9+\u5FAE\u535A" },
  { query: "\u63CF\u8FF0\u4E00\u4E0B\u6211\u7684\u4E00\u5929", expectedIndex: [20, 64, 72, 65, 66], type: "semantic", description: "\u4E00\u5929\u2192\u8D77\u5E8A+\u5496\u5561+\u5730\u94C1+\u98DF\u5802+B\u7AD9" },
  // Negative / exclusion queries
  { query: "\u6211\u6709\u4EC0\u4E48\u4E0D\u559C\u6B22\u5403\u7684", expectedIndex: 51, type: "semantic", description: "\u4E0D\u559C\u6B22\u5403\u2192\u9999\u83DC" },
  { query: "\u6211\u4E0D\u64C5\u957F\u4EC0\u4E48", expectedIndex: [75, 47], type: "semantic", description: "\u4E0D\u64C5\u957F\u2192\u5F00\u8F66/\u5C0F\u63D0\u7434" },
  // Temporal queries
  { query: "\u6211\u6700\u8FD1\u5728\u5B66\u4EC0\u4E48\u65B0\u4E1C\u897F", expectedIndex: [7, 33], type: "semantic", description: "\u5B66\u65B0\u4E1C\u897F\u2192Rust+\u65E5\u8BED" },
  { query: "\u6211\u6700\u8FD1\u82B1\u94B1\u4E70\u4E86\u4EC0\u4E48", expectedIndex: [71, 69], type: "semantic", description: "\u6700\u8FD1\u82B1\u94B1\u2192\u76F2\u76D2/\u53CC\u5341\u4E00" },
  // Abstract personality queries
  { query: "\u6211\u7684\u6027\u683C\u7279\u70B9\u662F\u4EC0\u4E48", expectedIndex: [52, 26, 58], type: "semantic", description: "\u6027\u683C\u2192\u6015\u51B7+\u6015\u86C7+\u6015\u6253\u9488" },
  { query: "\u6211\u662F\u4E00\u4E2A\u600E\u6837\u7684\u4EBA", expectedIndex: [0, 56, 60], type: "semantic", description: "\u600E\u6837\u7684\u4EBA\u2192\u5DE5\u4F5C+\u7AE5\u5E74+\u68A6\u60F3" },
  // Cross-domain queries
  { query: "\u6211\u5728\u7F51\u4E0A\u82B1\u591A\u5C11\u65F6\u95F4", expectedIndex: [40, 66, 67], type: "semantic", description: "\u7F51\u4E0A\u65F6\u95F4\u2192\u6296\u97F3+B\u7AD9+\u5FAE\u535A" },
  { query: "\u6211\u6709\u54EA\u4E9B\u56FA\u5B9A\u5F00\u652F", expectedIndex: [11, 68], type: "semantic", description: "\u56FA\u5B9A\u5F00\u652F\u2192\u623F\u8D37+\u7F51\u8D2D" },
  { query: "\u6211\u90FD\u5BB3\u6015\u4EC0\u4E48", expectedIndex: [26, 58, 52], type: "semantic", description: "\u5BB3\u6015\u2192\u86C7+\u6253\u9488+\u51B7" },
  { query: "\u6211\u7684\u793E\u4EA4\u6D3B\u52A8", expectedIndex: [14, 36, 46], type: "semantic", description: "\u793E\u4EA4\u2192\u7BEE\u7403+\u7FBD\u6BDB\u7403+\u6F14\u5531\u4F1A" },
  { query: "\u6211\u5B66\u8FC7\u54EA\u4E9B\u6280\u80FD", expectedIndex: [7, 33, 47], type: "semantic", description: "\u6280\u80FD\u2192Rust+\u65E5\u8BED+\u5C0F\u63D0\u7434" },
  { query: "\u6211\u7684\u996E\u98DF\u504F\u597D", expectedIndex: [17, 51, 48], type: "semantic", description: "\u996E\u98DF\u2192\u5403\u8FA3+\u4E0D\u5403\u9999\u83DC+\u7CD6\u918B\u6392\u9AA8" },
  { query: "\u6211\u6709\u4EC0\u4E48\u7ECF\u6D4E\u8D1F\u62C5", expectedIndex: [11, 32, 68], type: "semantic", description: "\u7ECF\u6D4E\u8D1F\u62C5\u2192\u623F\u8D37+\u4E8F\u94B1+\u7F51\u8D2D" },
  { query: "\u6211\u5BF9\u672A\u6765\u6709\u4EC0\u4E48\u89C4\u5212", expectedIndex: [60, 61, 62, 63], type: "semantic", description: "\u672A\u6765\u89C4\u5212\u2192\u5496\u5561\u5E97+PMP+\u6512\u94B1+\u76D6\u623F" },
  { query: "\u6211\u5728\u5B57\u8282\u505A\u4EC0\u4E48\u5C97\u4F4D", expectedIndex: [0, 39], type: "direct", description: "\u5B57\u8282\u5C97\u4F4D\u2192\u540E\u7AEF/\u5B89\u5168" },
  { query: "\u548C\u5C0F\u96E8\u7684\u5173\u7CFB\u8FDB\u5C55", expectedIndex: [1, 12], type: "direct", description: "\u5C0F\u96E8\u2192\u5728\u4E00\u8D77+\u6000\u5B55" },
  { query: "\u6211\u5750\u51E0\u53F7\u7EBF\u5730\u94C1", expectedIndex: 72, type: "direct", description: "\u51E0\u53F7\u7EBF\u21922\u8F6C10" },
  { query: "\u6211\u5728 36kr \u4E0A\u770B\u4EC0\u4E48", expectedIndex: 76, type: "direct", description: "36kr\u2192\u79D1\u6280\u65B0\u95FB" },
  // ── Additional direct queries to reach 100 ──
  { query: "\u6211\u7684\u6296\u97F3\u4F7F\u7528\u65F6\u95F4", expectedIndex: 40, type: "direct", description: "\u6296\u97F3\u65F6\u95F4\u2192\u4E24\u5C0F\u65F6" },
  { query: "\u5468\u6770\u4F26\u7684\u6B4C\u6211\u542C\u4E86\u591A\u4E45", expectedIndex: 44, type: "direct", description: "\u5468\u6770\u4F26\u2192\u4E8C\u5341\u5E74" },
  { query: "\u7CD6\u918B\u6392\u9AA8\u662F\u6211\u505A\u7684\u5417", expectedIndex: 48, type: "direct", description: "\u7CD6\u918B\u6392\u9AA8\u2192\u62FF\u624B\u83DC" },
  { query: "\u51AC\u5929\u6211\u613F\u610F\u51FA\u95E8\u5417", expectedIndex: 52, type: "direct", description: "\u51AC\u5929\u51FA\u95E8\u2192\u4E0D\u613F\u610F" },
  { query: "\u6211\u5C0F\u65F6\u5019\u53BB\u6CB3\u91CC\u5E72\u561B", expectedIndex: 56, type: "direct", description: "\u6CB3\u91CC\u2192\u6478\u9C7C" },
  { query: "\u6211\u60F3\u5F00\u4EC0\u4E48\u5E97", expectedIndex: 60, type: "direct", description: "\u5F00\u5E97\u2192\u5496\u5561\u5E97" },
  { query: "\u6211\u65E9\u996D\u524D\u5148\u5E72\u561B", expectedIndex: 64, type: "direct", description: "\u65E9\u996D\u524D\u2192\u559D\u5496\u5561" },
  { query: "\u6211\u7F51\u8D2D\u4E00\u822C\u82B1\u591A\u5C11", expectedIndex: 68, type: "direct", description: "\u7F51\u8D2D\u91D1\u989D\u21923000" },
  { query: "\u6211\u5750\u5730\u94C1\u8F6C\u54EA\u6761\u7EBF", expectedIndex: 72, type: "direct", description: "\u8F6C\u7EBF\u21922\u8F6C10" },
  { query: "\u6211\u6BCF\u5929\u770B 36kr \u5417", expectedIndex: 76, type: "direct", description: "36kr\u2192\u6BCF\u5929\u770B" },
  { query: "\u4E94\u6708\u5929\u7684\u6F14\u5531\u4F1A\u4EC0\u4E48\u65F6\u5019\u53BB\u7684", expectedIndex: 46, type: "direct", description: "\u4E94\u6708\u5929\u2192\u4E0A\u4E2A\u6708" },
  { query: "\u63D0\u62C9\u7C73\u82CF\u662F\u6211\u6700\u8FD1\u5B66\u7684\u5417", expectedIndex: 50, type: "direct", description: "\u63D0\u62C9\u7C73\u82CF\u2192\u4E0A\u5468\u5B66\u4F1A" },
  { query: "\u6211\u53BB\u5E74\u590F\u5929\u4E2D\u6691\u4E86\u5417", expectedIndex: 55, type: "direct", description: "\u4E2D\u6691\u2192\u53BB\u5E74\u590F\u5929" },
  { query: "PMP \u4EC0\u4E48\u65F6\u5019\u8003", expectedIndex: 61, type: "direct", description: "PMP\u2192\u660E\u5E74" },
  { query: "\u6211\u901A\u52E4\u8981\u591A\u957F\u65F6\u95F4", expectedIndex: 73, type: "direct", description: "\u901A\u52E4\u65F6\u95F4\u2192\u4E00\u4E2A\u534A\u5C0F\u65F6" },
  // ── Additional semantic queries to reach 100 ──
  { query: "\u6211\u7684\u7AE5\u5E74\u4F19\u4F34", expectedIndex: 59, type: "semantic", description: "\u7AE5\u5E74\u4F19\u4F34\u2192\u65FA\u8D22" },
  { query: "\u6211\u5BF9\u4EC0\u4E48\u98DF\u7269\u53CD\u611F", expectedIndex: 51, type: "semantic", description: "\u98DF\u7269\u53CD\u611F\u2192\u9999\u83DC" },
  { query: "\u6211\u6709\u4EC0\u4E48\u5185\u5BB9\u521B\u4F5C\u7ECF\u5386", expectedIndex: 41, type: "semantic", description: "\u5185\u5BB9\u521B\u4F5C\u2192\u6280\u672F\u535A\u5BA2" },
  { query: "\u6211\u7684\u7406\u8D22\u7ECF\u5386", expectedIndex: [32, 62], type: "semantic", description: "\u7406\u8D22\u2192\u7092\u80A1\u4E8F\u94B1+\u6512\u94B1\u76EE\u6807" },
  // ════════════════════════════════════════════════════════════
  // NEW DIRECT QUERIES (100 more, for memories 80-199)
  // ════════════════════════════════════════════════════════════
  // Memory 80-99: Work details direct
  { query: "\u6211\u8D1F\u8D23\u4EC0\u4E48\u7CFB\u7EDF", expectedIndex: 80, type: "direct", description: "\u7CFB\u7EDF\u2192\u98CE\u63A7" },
  { query: "\u6211\u4EEC\u7EC4\u7528\u4EC0\u4E48\u6280\u672F\u6808", expectedIndex: 81, type: "direct", description: "\u6280\u672F\u6808\u2192Go+gRPC+Kafka" },
  { query: "\u6211\u7684 leader \u53EB\u4EC0\u4E48", expectedIndex: 82, type: "direct", description: "leader\u2192\u738B\u78CA" },
  { query: "\u6211\u4E0A\u4E2A\u5B63\u5EA6\u7EE9\u6548\u600E\u4E48\u6837", expectedIndex: 83, type: "direct", description: "\u7EE9\u6548\u2192B+" },
  { query: "\u674E\u6668\u662F\u8C01", expectedIndex: 84, type: "direct", description: "\u674E\u6668\u2192\u540C\u4E8B\u597D\u53CB" },
  { query: "\u516C\u53F8\u7ED9\u6211\u914D\u4E86\u4EC0\u4E48\u8BBE\u5907", expectedIndex: 85, type: "direct", description: "\u8BBE\u5907\u2192\u4E24\u57574K\u663E\u793A\u5668" },
  { query: "\u6211\u4E4B\u524D\u5728\u54EA\u5BB6\u516C\u53F8", expectedIndex: 86, type: "direct", description: "\u4E4B\u524D\u516C\u53F8\u2192\u7F8E\u56E2" },
  { query: "\u5165\u804C\u5B57\u8282\u6DA8\u4E86\u591A\u5C11\u85AA\u6C34", expectedIndex: 87, type: "direct", description: "\u6DA8\u85AA\u219240%" },
  { query: "\u6211\u4EEC\u591A\u4E45\u5F00\u4E00\u6B21 sprint review", expectedIndex: 88, type: "direct", description: "sprint\u2192\u4E24\u5468\u4E00\u6B21" },
  { query: "\u6211\u6700\u8FD1\u5728\u505A\u4EC0\u4E48 POC", expectedIndex: 89, type: "direct", description: "POC\u2192\u53CD\u6B3A\u8BC8\u6A21\u578B" },
  { query: "\u6211\u5B9E\u4E60\u5728\u54EA\u5BB6\u516C\u53F8", expectedIndex: 90, type: "direct", description: "\u5B9E\u4E60\u2192\u767E\u5EA6" },
  { query: "\u516C\u53F8\u697C\u4E0B\u6709\u4EC0\u4E48\u5E97", expectedIndex: 91, type: "direct", description: "\u697C\u4E0B\u2192\u661F\u5DF4\u514B" },
  { query: "\u4F60\u5728\u516C\u53F8\u6234\u4EC0\u4E48\u8033\u673A", expectedIndex: 92, type: "direct", description: "\u8033\u673A\u2192\u964D\u566A" },
  { query: "\u88AB CTO \u8868\u626C\u662F\u56E0\u4E3A\u4EC0\u4E48", expectedIndex: 93, type: "direct", description: "CTO\u8868\u626C\u2192\u67B6\u6784\u4F18\u5316" },
  { query: "\u5C0F\u9648\u53BB\u4E86\u54EA\u5BB6\u516C\u53F8", expectedIndex: 94, type: "direct", description: "\u5C0F\u9648\u2192\u5FEB\u624B" },
  { query: "\u4F60\u5728\u51C6\u5907\u4EC0\u4E48\u8FF0\u804C", expectedIndex: 95, type: "direct", description: "\u8FF0\u804C\u2192\u664B\u5347\u8BC4\u5BA1" },
  { query: "\u4F60\u6709\u51E0\u5E74 Go \u7ECF\u9A8C", expectedIndex: 96, type: "direct", description: "Go\u7ECF\u9A8C\u21923\u5E74" },
  { query: "\u5B57\u8282\u6709\u4EC0\u4E48\u798F\u5229", expectedIndex: 97, type: "direct", description: "\u798F\u5229\u2192\u4E09\u9910\u5065\u8EAB\u623F\u4F53\u68C0" },
  { query: "\u4F60 GitHub \u6709\u591A\u5C11 star", expectedIndex: 98, type: "direct", description: "GitHub\u21921200 star" },
  { query: "\u5E74\u4F1A\u4F60\u62BD\u5230\u4E86\u4EC0\u4E48", expectedIndex: 99, type: "direct", description: "\u5E74\u4F1A\u2192iPad Pro" },
  // Memory 100-119: Family direct
  { query: "\u4F60\u7238\u662F\u505A\u4EC0\u4E48\u7684", expectedIndex: 100, type: "direct", description: "\u7238\u7238\u2192\u6570\u5B66\u8001\u5E08" },
  { query: "\u4F60\u5988\u5728\u54EA\u5DE5\u4F5C", expectedIndex: 101, type: "direct", description: "\u5988\u5988\u2192\u8D85\u5E02\u6536\u94F6\u5458" },
  { query: "\u4F60\u6709\u5144\u5F1F\u59D0\u59B9\u5417", expectedIndex: 102, type: "direct", description: "\u5144\u59B9\u2192\u59B9\u59B9\u5C0F\u654F" },
  { query: "\u4F60\u59B9\u59B9\u7ED3\u5A5A\u4E86\u5417", expectedIndex: 103, type: "direct", description: "\u59B9\u59B9\u5A5A\u4E8B\u2192\u53BB\u5E74\u7ED3\u5A5A" },
  { query: "\u4F60\u7237\u7237\u8FD8\u5728\u5417", expectedIndex: 104, type: "direct", description: "\u7237\u7237\u2192\u53BB\u5E74\u8FC7\u4E16" },
  { query: "\u4F60\u5976\u5976\u8EAB\u4F53\u600E\u4E48\u6837", expectedIndex: 105, type: "direct", description: "\u5976\u5976\u2192\u8FD8\u597D\u72EC\u5C45" },
  { query: "\u4F60\u4EEC\u8FC7\u5E74\u5728\u54EA\u8FC7", expectedIndex: 106, type: "direct", description: "\u8FC7\u5E74\u2192\u957F\u6C99\u8001\u5BB6" },
  { query: "\u4F60\u7238\u6709\u4EC0\u4E48\u75C5", expectedIndex: 107, type: "direct", description: "\u7238\u7238\u75C5\u2192\u9AD8\u8840\u538B" },
  { query: "\u5C0F\u96E8\u7684\u7236\u6BCD\u5728\u54EA", expectedIndex: 108, type: "direct", description: "\u5C0F\u96E8\u7236\u6BCD\u2192\u676D\u5DDE" },
  { query: "\u4F60\u7684\u623F\u5B50\u5728\u54EA", expectedIndex: 109, type: "direct", description: "\u623F\u5B50\u2192\u660C\u5E73\u56DE\u9F99\u89C2" },
  { query: "\u4F60\u53D4\u53D4\u505A\u4EC0\u4E48\u751F\u610F", expectedIndex: 110, type: "direct", description: "\u53D4\u53D4\u2192\u6E58\u83DC\u9986" },
  { query: "\u4F60\u8868\u54E5\u5728\u5E72\u561B", expectedIndex: 111, type: "direct", description: "\u8868\u54E5\u2192\u90E8\u961F\u8FDE\u957F" },
  { query: "\u4F60\u5988\u50AC\u4F60\u4EC0\u4E48", expectedIndex: 112, type: "direct", description: "\u50AC\u5A5A\u2192\u7ED3\u5A5A" },
  { query: "\u5C0F\u96E8\u7ED9\u4F60\u5988\u4E70\u4E86\u4EC0\u4E48", expectedIndex: 113, type: "direct", description: "\u5C0F\u96E8\u9001\u793C\u2192\u91D1\u9879\u94FE" },
  { query: "\u4F60\u8868\u5F1F\u4ECA\u5E74\u5E72\u561B", expectedIndex: 114, type: "direct", description: "\u8868\u5F1F\u2192\u9AD8\u8003" },
  { query: "\u4F60\u6E05\u660E\u8282\u505A\u4EC0\u4E48", expectedIndex: 115, type: "direct", description: "\u6E05\u660E\u2192\u626B\u5893" },
  { query: "\u5BB6\u91CC\u517B\u4E86\u4EC0\u4E48\u690D\u7269", expectedIndex: 116, type: "direct", description: "\u690D\u7269\u2192\u7EFF\u841D\u91D1\u9C7C" },
  { query: "\u4F60\u7238\u9000\u4F11\u540E\u5E72\u561B", expectedIndex: 117, type: "direct", description: "\u7238\u9000\u4F11\u2192\u9493\u9C7C" },
  { query: "\u4F60\u59B9\u59B9\u6000\u5B55\u4E86\u5417", expectedIndex: 118, type: "direct", description: "\u59B9\u59B9\u6000\u5B55\u2192\u4E24\u4E2A\u6708" },
  { query: "\u4F60\u548C\u5C0F\u96E8\u4EC0\u4E48\u65F6\u5019\u9886\u8BC1", expectedIndex: 119, type: "direct", description: "\u9886\u8BC1\u2192\u660E\u5E74" },
  // Memory 120-139: Health/Finance/Education direct
  { query: "\u4F60\u6709\u80C3\u75C5\u5417", expectedIndex: 120, type: "direct", description: "\u80C3\u75C5\u2192\u6162\u6027\u80C3\u708E" },
  { query: "\u4F60\u591A\u4E45\u505A\u4E00\u6B21\u80C3\u955C", expectedIndex: 121, type: "direct", description: "\u80C3\u955C\u2192\u534A\u5E74" },
  { query: "\u4F60\u5403\u4EC0\u4E48\u836F", expectedIndex: 122, type: "direct", description: "\u836F\u2192\u5965\u7F8E\u62C9\u5511\u83AB\u6C99\u5FC5\u5229" },
  { query: "\u4F60\u7532\u72B6\u817A\u6709\u95EE\u9898\u5417", expectedIndex: 123, type: "direct", description: "\u7532\u72B6\u817A\u2192\u7ED3\u8282" },
  { query: "\u4F60\u8170\u6709\u4EC0\u4E48\u95EE\u9898", expectedIndex: 124, type: "direct", description: "\u8170\u2192\u690E\u95F4\u76D8\u7A81\u51FA" },
  { query: "\u4F60\u7684\u6905\u5B50\u591A\u5C11\u94B1", expectedIndex: 125, type: "direct", description: "\u6905\u5B50\u2192Herman Miller 8000" },
  { query: "\u4F60\u4E70\u4E86\u4EC0\u4E48\u57FA\u91D1", expectedIndex: 126, type: "direct", description: "\u57FA\u91D1\u2192\u8D27\u5E01\u57FA\u91D110\u4E07" },
  { query: "\u4F60\u6BCF\u6708\u5B9A\u6295\u591A\u5C11", expectedIndex: 127, type: "direct", description: "\u5B9A\u6295\u2192\u6CAA\u6DF1300 3000" },
  { query: "\u4F60\u4E70\u4E86\u4EC0\u4E48\u4FDD\u9669", expectedIndex: 128, type: "direct", description: "\u4FDD\u9669\u2192\u767E\u4E07\u533B\u7597+\u91CD\u75BE" },
  { query: "\u4F60\u9000\u7A0E\u9000\u4E86\u591A\u5C11", expectedIndex: 129, type: "direct", description: "\u9000\u7A0E\u21924800" },
  { query: "\u4F60\u516C\u79EF\u91D1\u591A\u5C11", expectedIndex: 130, type: "direct", description: "\u516C\u79EF\u91D1\u21923200" },
  { query: "\u4F60\u5728\u54EA\u4E2A\u5927\u5B66", expectedIndex: 131, type: "direct", description: "\u5927\u5B66\u2192\u6B66\u6C49\u5927\u5B66" },
  { query: "\u4F60\u6BD5\u4E1A\u8BBE\u8BA1\u505A\u4E86\u4EC0\u4E48", expectedIndex: 132, type: "direct", description: "\u6BD5\u8BBE\u2192\u4EBA\u8138\u8BC6\u522B" },
  { query: "\u4F60\u5927\u5B66\u8001\u5E08\u8C01\u8BB2\u8BFE\u597D", expectedIndex: 133, type: "direct", description: "\u8001\u5E08\u2192\u5468\u8001\u5E08\u6570\u636E\u7ED3\u6784" },
  { query: "\u4F60\u8003\u7814\u8003\u4E86\u51E0\u6B21", expectedIndex: 134, type: "direct", description: "\u8003\u7814\u2192\u4E24\u6B21\u5DEE3\u5206" },
  { query: "\u4F60\u4E3A\u4EC0\u4E48\u6CA1\u8BFB\u7814", expectedIndex: 135, type: "direct", description: "\u6CA1\u8BFB\u7814\u2192\u653E\u5F03\u5DE5\u4F5C\u4E86" },
  { query: "\u4F60\u9AD8\u4E2D\u5728\u54EA\u8BFB\u7684", expectedIndex: 136, type: "direct", description: "\u9AD8\u4E2D\u2192\u957F\u6C99\u4E00\u4E2D" },
  { query: "\u4F60\u4FE1\u7528\u5361\u989D\u5EA6\u591A\u5C11", expectedIndex: 137, type: "direct", description: "\u4FE1\u7528\u5361\u21925\u4E07" },
  { query: "\u4F60\u5728\u7406\u8D22\u901A\u6709\u591A\u5C11\u5B58\u6B3E", expectedIndex: 138, type: "direct", description: "\u7406\u8D22\u901A\u21925\u4E07\u5B9A\u671F" },
  { query: "\u4F60\u5230\u624B\u5DE5\u8D44\u591A\u5C11", expectedIndex: 139, type: "direct", description: "\u5230\u624B\u21922.8\u4E07" },
  // Memory 140-159: Social/Hobby/Routine direct
  { query: "\u9AD8\u4E2D\u540C\u5B66\u7FA4\u8C01\u6700\u6D3B\u8DC3", expectedIndex: 140, type: "direct", description: "\u7FA4\u6D3B\u8DC3\u2192\u8001\u8D75" },
  { query: "\u5218\u6BC5\u5728\u505A\u4EC0\u4E48", expectedIndex: 141, type: "direct", description: "\u5218\u6BC5\u2192\u6DF1\u5733SaaS\u521B\u4E1A" },
  { query: "\u4F60\u548C\u540C\u5B66\u73A9\u4EC0\u4E48\u6E38\u620F", expectedIndex: 142, type: "direct", description: "\u540C\u5B66\u6E38\u620F\u2192\u72FC\u4EBA\u6740" },
  { query: "\u4F60\u90BB\u5C45\u662F\u4EC0\u4E48\u4EBA", expectedIndex: 143, type: "direct", description: "\u90BB\u5C45\u2192\u9000\u4F11\u592B\u5987" },
  { query: "\u9ED1\u5BA2\u9A6C\u62C9\u677E\u62FF\u4E86\u4EC0\u4E48\u5956", expectedIndex: 144, type: "direct", description: "\u9ED1\u5BA2\u9A6C\u62C9\u677E\u2192\u4E8C\u7B49\u5956" },
  { query: "\u4F60\u5728 LeetCode \u5237\u4E86\u591A\u5C11\u9898", expectedIndex: 145, type: "direct", description: "LeetCode\u2192600\u9898" },
  { query: "\u4F60\u4E70\u4E86\u51E0\u628A\u673A\u68B0\u952E\u76D8", expectedIndex: 146, type: "direct", description: "\u673A\u68B0\u952E\u76D8\u2192\u4E09\u628A" },
  { query: "\u4F60\u539F\u795E\u4EC0\u4E48\u89D2\u8272\u6EE1\u547D", expectedIndex: 147, type: "direct", description: "\u539F\u795E\u2192\u96F7\u7535\u5C06\u519B" },
  { query: "\u4F60\u5468\u65E5\u4E0B\u5348\u4E00\u822C\u5E72\u561B", expectedIndex: 148, type: "direct", description: "\u5468\u65E5\u2192\u5496\u5561\u9986\u770B\u4E66" },
  { query: "\u4F60\u95F9\u949F\u51E0\u70B9\u54CD", expectedIndex: 149, type: "direct", description: "\u95F9\u949F\u21926:50" },
  { query: "\u8D70\u5230\u5730\u94C1\u7AD9\u8981\u591A\u4E45", expectedIndex: 150, type: "direct", description: "\u8D70\u8DEF\u219215\u5206\u949F" },
  { query: "\u4F60\u5348\u4F11\u600E\u4E48\u4F11\u606F", expectedIndex: 151, type: "direct", description: "\u5348\u4F11\u2192\u8DB4\u684C\u4E0A\u534A\u5C0F\u65F6" },
  { query: "\u4F60\u4E0B\u5348\u559D\u4EC0\u4E48", expectedIndex: 152, type: "direct", description: "\u4E0B\u5348\u2192\u4E09\u70B9\u5496\u5561" },
  { query: "\u4F60\u665A\u996D\u5E38\u70B9\u4EC0\u4E48\u5916\u5356", expectedIndex: 153, type: "direct", description: "\u5916\u5356\u2192\u9EC4\u7116\u9E21" },
  { query: "\u4F60\u6D17\u5B8C\u5934\u7528\u5439\u98CE\u673A\u5417", expectedIndex: 154, type: "direct", description: "\u5439\u98CE\u673A\u2192\u5B8C\u5168\u5439\u5E72" },
  { query: "\u4F60\u51E0\u70B9\u5F00\u59CB\u6D17\u6F31", expectedIndex: 155, type: "direct", description: "\u6D17\u6F31\u2192\u5341\u70B9\u534A" },
  { query: "\u4F60\u5065\u8EAB\u623F\u7684\u5E74\u5361\u7528\u4E86\u5417", expectedIndex: 156, type: "direct", description: "\u5065\u8EAB\u623F\u2192\u53BB\u4E86\u4E94\u6B21" },
  { query: "\u4F60\u624B\u673A\u6709\u591A\u5C11\u7167\u7247", expectedIndex: 157, type: "direct", description: "\u7167\u7247\u21922\u4E07\u591A\u5F20" },
  { query: "\u4F60\u7528\u4EC0\u4E48\u505A\u77E5\u8BC6\u7BA1\u7406", expectedIndex: 158, type: "direct", description: "\u77E5\u8BC6\u7BA1\u7406\u2192Notion" },
  { query: "\u4F60\u5468\u4E09\u665A\u4E0A\u548C\u5C0F\u96E8\u5E72\u561B", expectedIndex: 159, type: "direct", description: "\u5468\u4E09\u2192\u770B\u7EFC\u827A" },
  // Memory 160-179: Personality/Life events direct
  { query: "\u4F60\u813E\u6C14\u600E\u4E48\u6837", expectedIndex: 160, type: "direct", description: "\u813E\u6C14\u2192\u6025\u8E81\u76F4\u63A5" },
  { query: "\u9047\u5230\u4E0D\u516C\u5E73\u7684\u4E8B\u4F60\u600E\u4E48\u529E", expectedIndex: 161, type: "direct", description: "\u4E0D\u516C\u5E73\u2192\u5F53\u9762\u8BF4" },
  { query: "\u4F60\u4E70\u4E1C\u897F\u524D\u505A\u4EC0\u4E48", expectedIndex: 162, type: "direct", description: "\u4E70\u4E1C\u897F\u2192\u770B\u6D4B\u8BC4\u5BF9\u6BD4" },
  { query: "\u4F60\u559C\u6B22\u5927\u578B\u805A\u4F1A\u5417", expectedIndex: 163, type: "direct", description: "\u805A\u4F1A\u2192\u8D85\u5341\u4EBA\u4E0D\u81EA\u5728" },
  { query: "\u4F60\u7528\u4EC0\u4E48\u7BA1\u7406\u5F85\u529E\u4E8B\u9879", expectedIndex: 164, type: "direct", description: "\u5F85\u529E\u2192\u6EF4\u7B54\u6E05\u5355" },
  { query: "\u4F60\u538B\u529B\u5927\u7684\u65F6\u5019\u600E\u4E48\u529E", expectedIndex: 165, type: "direct", description: "\u538B\u529B\u2192\u53BB\u6C5F\u8FB9\u8D70" },
  { query: "\u4F60\u4EC0\u4E48\u65F6\u5019\u642C\u5230\u5317\u4EAC\u7684", expectedIndex: 166, type: "direct", description: "\u642C\u5317\u4EAC\u21922022\u5E74" },
  { query: "\u4F60\u5728\u4E0A\u6D77\u4F4F\u54EA", expectedIndex: 167, type: "direct", description: "\u4E0A\u6D77\u2192\u6D66\u4E1C\u5F20\u6C5F" },
  { query: "\u4F60\u53BB\u5E74\u56FD\u5E86\u53BB\u4E86\u54EA", expectedIndex: 168, type: "direct", description: "\u56FD\u5E86\u2192\u897F\u5B89" },
  { query: "\u4F60\u871C\u6708\u6253\u7B97\u53BB\u54EA", expectedIndex: 169, type: "direct", description: "\u871C\u6708\u2192\u9A6C\u5C14\u4EE3\u592B" },
  { query: "\u4F60\u5927\u5B66\u65F6\u5019\u53BB\u8FC7\u4E91\u5357\u5417", expectedIndex: 170, type: "direct", description: "\u4E91\u5357\u2192\u80CC\u5305\u534A\u4E2A\u6708" },
  { query: "\u4F60\u51FA\u5DEE\u53BB\u8FC7\u54EA\u4E9B\u57CE\u5E02", expectedIndex: 171, type: "direct", description: "\u51FA\u5DEE\u2192\u6DF1\u5733\u5E7F\u5DDE\u6210\u90FD" },
  { query: "\u4F60\u6709\u9009\u62E9\u56F0\u96BE\u75C7\u5417", expectedIndex: 172, type: "direct", description: "\u9009\u62E9\u56F0\u96BE\u2192\u70B9\u5916\u5356\u7EA0\u7ED3" },
  { query: "\u4F60\u624B\u673A\u662F\u9759\u97F3\u7684\u5417", expectedIndex: 173, type: "direct", description: "\u624B\u673A\u2192\u9759\u97F3\u6F0F\u63A5" },
  { query: "\u4F60\u4F1A\u4E3B\u52A8\u6C42\u4EBA\u5E2E\u5FD9\u5417", expectedIndex: 174, type: "direct", description: "\u6C42\u4EBA\u2192\u4E0D\u559C\u6B22\u9EBB\u70E6\u522B\u4EBA" },
  { query: "\u4F60\u60C5\u7EEA\u4E0D\u597D\u4F1A\u600E\u6837", expectedIndex: 175, type: "direct", description: "\u60C5\u7EEA\u5DEE\u2192\u66B4\u996E\u66B4\u98DF" },
  { query: "\u4F60\u6709\u6F5C\u6C34\u8BC1\u5417", expectedIndex: 176, type: "direct", description: "\u6F5C\u6C34\u2192PADI OW" },
  { query: "\u4F60\u751F\u65E5\u6536\u5230\u4E86\u4EC0\u4E48\u793C\u7269", expectedIndex: 177, type: "direct", description: "\u751F\u65E5\u2192Apple Watch" },
  { query: "\u4F60\u548C\u524D\u5973\u53CB\u4E3A\u4EC0\u4E48\u5206\u624B", expectedIndex: 178, type: "direct", description: "\u524D\u5973\u53CB\u2192\u5F02\u5730\u604B" },
  { query: "\u4F60\u7B2C\u4E00\u4EFD\u5DE5\u4F5C\u5728\u54EA", expectedIndex: 179, type: "direct", description: "\u7B2C\u4E00\u4EFD\u2192\u7F8E\u56E2\u5B9E\u4E60\u8F6C\u6B63" },
  // Memory 180-199: Specific details direct
  { query: "\u4F60\u7528\u4EC0\u4E48\u624B\u673A", expectedIndex: 180, type: "direct", description: "\u624B\u673A\u2192iPhone 15 Pro Max" },
  { query: "\u4F60\u6700\u8BA8\u538C\u88AB\u95EE\u4EC0\u4E48", expectedIndex: 181, type: "direct", description: "\u8BA8\u538C\u95EE\u2192\u4EC0\u4E48\u65F6\u5019\u7ED3\u5A5A" },
  { query: "\u4F60\u7528\u4EC0\u4E48 App \u542C\u6B4C", expectedIndex: 182, type: "direct", description: "\u542C\u6B4C\u2192Spotify" },
  { query: "\u4F60\u5496\u5561\u600E\u4E48\u559D", expectedIndex: 183, type: "direct", description: "\u5496\u5561\u2192\u7F8E\u5F0F\u4E0D\u52A0\u7CD6\u5976" },
  { query: "\u4F60\u901A\u52E4\u65F6\u542C\u4EC0\u4E48", expectedIndex: 184, type: "direct", description: "\u901A\u52E4\u542C\u2192\u64AD\u5BA2" },
  { query: "\u4F60\u6700\u8FD1\u542C\u4EC0\u4E48\u64AD\u5BA2", expectedIndex: 185, type: "direct", description: "\u64AD\u5BA2\u2192\u786C\u5730\u9A87\u5BA2" },
  { query: "\u4F60\u4EC0\u4E48\u65F6\u5019\u4E70\u4E66", expectedIndex: 186, type: "direct", description: "\u4E70\u4E66\u2192618\u53CC\u5341\u4E00" },
  { query: "\u4F60\u60F3\u4E70\u4EC0\u4E48\u76F8\u673A", expectedIndex: 187, type: "direct", description: "\u76F8\u673A\u2192\u5BCC\u58EBX-T5" },
  { query: "\u4F60\u642C\u5BB6\u65F6\u6254\u4E86\u4EC0\u4E48", expectedIndex: 188, type: "direct", description: "\u642C\u5BB6\u2192\u65E7\u4E66\u8863\u670D" },
  { query: "\u4F60\u6709\u4EC0\u4E48\u8FD0\u52A8\u978B", expectedIndex: 189, type: "direct", description: "\u8FD0\u52A8\u978B\u2192Nike+Adidas" },
  { query: "\u4F60\u7761\u89C9\u5F00\u7A7A\u8C03\u5417", expectedIndex: 190, type: "direct", description: "\u7A7A\u8C03\u2192\u5FC5\u987B\u5F00" },
  { query: "\u4F60\u7528\u4EC0\u4E48\u6D4F\u89C8\u5668", expectedIndex: 191, type: "direct", description: "\u6D4F\u89C8\u5668\u2192Chrome" },
  { query: "\u4F60\u6709\u5F3A\u8FEB\u75C7\u5417", expectedIndex: 192, type: "direct", description: "\u5F3A\u8FEB\u2192\u53CD\u590D\u786E\u8BA4\u9501\u95E8" },
  { query: "\u4F60\u505A\u83DC\u653E\u849C\u591A\u5417", expectedIndex: 193, type: "direct", description: "\u849C\u2192\u653E\u5F88\u591A" },
  { query: "\u4F60\u591A\u4E45\u548C\u7238\u5988\u901A\u4E00\u6B21\u7535\u8BDD", expectedIndex: 194, type: "direct", description: "\u901A\u8BDD\u2192\u6BCF\u5468\u4E24\u6B21" },
  { query: "\u8BFB\u4E66\u4F1A\u4F60\u63A8\u8350\u4E86\u4EC0\u4E48\u4E66", expectedIndex: 195, type: "direct", description: "\u63A8\u8350\u2192\u9ED1\u5BA2\u4E0E\u753B\u5BB6" },
  { query: "\u4F60\u51AC\u5929\u7A7F\u4EC0\u4E48", expectedIndex: 196, type: "direct", description: "\u51AC\u5929\u7A7F\u2192\u7FBD\u7ED2\u670D" },
  { query: "\u4F60\u7ECF\u5E38\u53E3\u8154\u6E83\u75A1\u5417", expectedIndex: 197, type: "direct", description: "\u53E3\u8154\u6E83\u75A1\u2192\u7F3A\u7EF4B" },
  { query: "\u4F60\u5728\u641E\u4EC0\u4E48\u667A\u80FD\u5BB6\u5C45", expectedIndex: 198, type: "direct", description: "\u667A\u80FD\u5BB6\u5C45\u2192Home Assistant" },
  { query: "\u4F60\u548C\u5C0F\u96E8\u5468\u672B\u53BB\u54EA\u901B", expectedIndex: 199, type: "direct", description: "\u901B\u8857\u2192\u5B9C\u5BB6" },
  // ════════════════════════════════════════════════════════════
  // NEW SEMANTIC QUERIES (100 more, for memories 80-199)
  // ════════════════════════════════════════════════════════════
  // Work semantic
  { query: "\u4F60\u6BCF\u5929\u5904\u7406\u591A\u5C11\u6D41\u91CF", expectedIndex: 80, type: "semantic", description: "\u6D41\u91CF\u21922\u4EBF\u8BF7\u6C42" },
  { query: "\u4F60\u5728\u516C\u53F8\u7528\u4EC0\u4E48\u6D88\u606F\u961F\u5217", expectedIndex: 81, type: "semantic", description: "\u6D88\u606F\u961F\u5217\u2192Kafka" },
  { query: "\u4F60\u548C\u4E0A\u7EA7\u5173\u7CFB\u600E\u4E48\u6837", expectedIndex: 82, type: "semantic", description: "\u4E0A\u7EA7\u5173\u7CFB\u2192leader nice" },
  { query: "\u4F60\u4E0A\u6B21\u7EE9\u6548\u8003\u6838\u901A\u8FC7\u4E86\u5417", expectedIndex: 83, type: "semantic", description: "\u7EE9\u6548\u8003\u6838\u2192B+" },
  { query: "\u4F60\u5728\u516C\u53F8\u6709\u6CA1\u6709\u597D\u670B\u53CB", expectedIndex: 84, type: "semantic", description: "\u516C\u53F8\u670B\u53CB\u2192\u674E\u6668" },
  { query: "\u4F60\u505A\u5916\u5356\u76F8\u5173\u7684\u5DE5\u4F5C\u5417", expectedIndex: 86, type: "semantic", description: "\u5916\u5356\u2192\u7F8E\u56E2\u914D\u9001\u7B97\u6CD5" },
  { query: "\u4F60\u8DF3\u69FD\u6DA8\u4E86\u591A\u5C11", expectedIndex: 87, type: "semantic", description: "\u8DF3\u69FD\u2192\u6DA840%" },
  { query: "\u4F60\u5728\u641E\u673A\u5668\u5B66\u4E60\u5417", expectedIndex: 89, type: "semantic", description: "\u673A\u5668\u5B66\u4E60\u2192XGBoost POC" },
  { query: "\u4F60\u6709\u505A\u641C\u7D22\u5F15\u64CE\u7684\u7ECF\u9A8C\u5417", expectedIndex: 90, type: "semantic", description: "\u641C\u7D22\u2192\u767E\u5EA6\u641C\u7D22\u63A8\u8350" },
  { query: "\u4F60\u5728\u5F00\u6E90\u793E\u533A\u6D3B\u8DC3\u5417", expectedIndex: 98, type: "semantic", description: "\u5F00\u6E90\u2192GitHub 1200 star" },
  // Family semantic
  { query: "\u4F60\u7238\u662F\u4EC0\u4E48\u804C\u4E1A", expectedIndex: 100, type: "semantic", description: "\u7238\u804C\u4E1A\u2192\u6570\u5B66\u8001\u5E08" },
  { query: "\u4F60\u5988\u5FEB\u9000\u4F11\u4E86\u5417", expectedIndex: 101, type: "semantic", description: "\u9000\u4F11\u2192\u5988\u5988\u6536\u94F6\u5458" },
  { query: "\u4F60\u5BB6\u91CC\u6709\u51E0\u4E2A\u5B69\u5B50", expectedIndex: 102, type: "semantic", description: "\u51E0\u4E2A\u5B69\u5B50\u2192\u6709\u59B9\u59B9" },
  { query: "\u4F60\u5BB6\u6700\u8FD1\u6709\u559C\u4E8B\u5417", expectedIndex: [103, 118], type: "semantic", description: "\u559C\u4E8B\u2192\u59B9\u59B9\u7ED3\u5A5A/\u6000\u5B55" },
  { query: "\u5BB6\u91CC\u6709\u8001\u4EBA\u53BB\u4E16\u5417", expectedIndex: 104, type: "semantic", description: "\u53BB\u4E16\u2192\u7237\u7237" },
  { query: "\u4F60\u8FC7\u5E74\u600E\u4E48\u5B89\u6392", expectedIndex: 106, type: "semantic", description: "\u8FC7\u5E74\u2192\u56DE\u957F\u6C99" },
  { query: "\u4F60\u7238\u5988\u6709\u6162\u6027\u75C5\u5417", expectedIndex: 107, type: "semantic", description: "\u6162\u6027\u75C5\u2192\u7238\u9AD8\u8840\u538B" },
  { query: "\u4F60\u7684\u5A5A\u623F\u5728\u54EA", expectedIndex: 109, type: "semantic", description: "\u5A5A\u623F\u2192\u56DE\u9F99\u89C2" },
  { query: "\u4F60\u4EB2\u621A\u505A\u9910\u996E\u7684\u5417", expectedIndex: 110, type: "semantic", description: "\u9910\u996E\u2192\u53D4\u53D4\u6E58\u83DC\u9986" },
  { query: "\u4F60\u548C\u672A\u6765\u4E08\u6BCD\u5A18\u5173\u7CFB\u600E\u6837", expectedIndex: 108, type: "semantic", description: "\u4E08\u6BCD\u5A18\u2192\u676D\u5DDE" },
  // Health/Finance semantic
  { query: "\u4F60\u6709\u4EC0\u4E48\u6D88\u5316\u7CFB\u7EDF\u7684\u95EE\u9898", expectedIndex: 120, type: "semantic", description: "\u6D88\u5316\u2192\u6162\u6027\u80C3\u708E" },
  { query: "\u4F60\u5B9A\u671F\u505A\u4EC0\u4E48\u4F53\u68C0", expectedIndex: [121, 123], type: "semantic", description: "\u5B9A\u671F\u4F53\u68C0\u2192\u80C3\u955C/\u7532\u72B6\u817A" },
  { query: "\u4F60\u6BCF\u5929\u8981\u5403\u836F\u5417", expectedIndex: 122, type: "semantic", description: "\u6BCF\u5929\u5403\u836F\u2192\u5965\u7F8E\u62C9\u5511" },
  { query: "\u4F60\u4E45\u5750\u6709\u4EC0\u4E48\u6BDB\u75C5", expectedIndex: 124, type: "semantic", description: "\u4E45\u5750\u2192\u8170\u690E\u95F4\u76D8\u7A81\u51FA" },
  { query: "\u4F60\u82B1\u5927\u94B1\u4E70\u8FC7\u4EC0\u4E48\u529E\u516C\u8BBE\u5907", expectedIndex: 125, type: "semantic", description: "\u529E\u516C\u8BBE\u5907\u2192Herman Miller" },
  { query: "\u4F60\u7684\u5B58\u6B3E\u653E\u5728\u54EA", expectedIndex: [126, 138], type: "semantic", description: "\u5B58\u6B3E\u2192\u8682\u8681\u8D22\u5BCC/\u7406\u8D22\u901A" },
  { query: "\u4F60\u6709\u5B9A\u671F\u6295\u8D44\u4E60\u60EF\u5417", expectedIndex: 127, type: "semantic", description: "\u5B9A\u671F\u6295\u8D44\u2192\u5B9A\u6295" },
  { query: "\u4F60\u7684\u98CE\u9669\u4FDD\u969C", expectedIndex: 128, type: "semantic", description: "\u98CE\u9669\u4FDD\u969C\u2192\u767E\u4E07\u533B\u7597+\u91CD\u75BE" },
  { query: "\u4F60\u7A0E\u52A1\u65B9\u9762\u6709\u4EC0\u4E48\u7ECF\u5386", expectedIndex: 129, type: "semantic", description: "\u7A0E\u52A1\u2192\u9000\u7A0E4800" },
  { query: "\u4F60\u7684\u4F4F\u623F\u516C\u79EF\u91D1", expectedIndex: 130, type: "semantic", description: "\u4F4F\u623F\u516C\u79EF\u91D1\u21923200" },
  // Education semantic
  { query: "\u4F60\u62FF\u8FC7\u4EC0\u4E48\u5B66\u4E1A\u8363\u8A89", expectedIndex: 131, type: "semantic", description: "\u5B66\u4E1A\u8363\u8A89\u2192\u56FD\u5956" },
  { query: "\u4F60\u672C\u79D1\u7684\u6BD5\u4E1A\u9879\u76EE", expectedIndex: 132, type: "semantic", description: "\u6BD5\u4E1A\u9879\u76EE\u2192\u4EBA\u8138\u8BC6\u522B" },
  { query: "\u4F60\u5370\u8C61\u6700\u6DF1\u7684\u8001\u5E08", expectedIndex: [133, 136], type: "semantic", description: "\u5370\u8C61\u6DF1\u8001\u5E08\u2192\u5468\u8001\u5E08/\u5218\u8001\u5E08" },
  { query: "\u4F60\u8003\u7814\u5931\u8D25\u4E86\u5417", expectedIndex: 134, type: "semantic", description: "\u8003\u7814\u5931\u8D25\u2192\u5DEE3\u5206" },
  { query: "\u4F60\u8BFB\u4E86\u51E0\u5E74\u5B66", expectedIndex: [131, 136], type: "semantic", description: "\u8BFB\u4E66\u2192\u6B66\u5927+\u957F\u6C99\u4E00\u4E2D" },
  // Social/Hobby semantic
  { query: "\u4F60\u7684\u521B\u4E1A\u670B\u53CB", expectedIndex: 141, type: "semantic", description: "\u521B\u4E1A\u670B\u53CB\u2192\u5218\u6BC5SaaS" },
  { query: "\u4F60\u548C\u540C\u5B66\u600E\u4E48\u4FDD\u6301\u8054\u7CFB", expectedIndex: [140, 142], type: "semantic", description: "\u4FDD\u6301\u8054\u7CFB\u2192\u7FA4\u804A+\u72FC\u4EBA\u6740" },
  { query: "\u4F60\u548C\u90BB\u5C45\u5173\u7CFB\u597D\u5417", expectedIndex: 143, type: "semantic", description: "\u90BB\u5C45\u2192\u9000\u4F11\u592B\u5987\u9001\u83DC" },
  { query: "\u4F60\u6709\u4EC0\u4E48\u7F16\u7A0B\u6BD4\u8D5B\u7ECF\u5386", expectedIndex: 144, type: "semantic", description: "\u7F16\u7A0B\u6BD4\u8D5B\u2192\u9ED1\u5BA2\u9A6C\u62C9\u677E" },
  { query: "\u4F60\u7684\u7B97\u6CD5\u80FD\u529B\u600E\u4E48\u6837", expectedIndex: 145, type: "semantic", description: "\u7B97\u6CD5\u2192LeetCode 600\u9898" },
  { query: "\u4F60\u6709\u4EC0\u4E48\u5916\u8BBE\u7231\u597D", expectedIndex: 146, type: "semantic", description: "\u5916\u8BBE\u2192\u673A\u68B0\u952E\u76D8" },
  { query: "\u4F60\u73A9\u4EC0\u4E48\u624B\u6E38", expectedIndex: 147, type: "semantic", description: "\u624B\u6E38\u2192\u539F\u795E" },
  { query: "\u4F60\u5468\u672B\u6709\u4EC0\u4E48\u56FA\u5B9A\u5B89\u6392", expectedIndex: [148, 30], type: "semantic", description: "\u5468\u672B\u56FA\u5B9A\u2192\u770B\u4E66/\u966A\u5B69\u5B50" },
  { query: "\u4F60\u8D56\u5E8A\u5417", expectedIndex: 149, type: "semantic", description: "\u8D56\u5E8A\u2192\u5341\u5206\u949F" },
  { query: "\u4F60\u4E2D\u5348\u600E\u4E48\u6062\u590D\u7CBE\u529B", expectedIndex: 151, type: "semantic", description: "\u6062\u590D\u7CBE\u529B\u2192\u5348\u4F11\u8DB4\u684C\u4E0A" },
  // Personality/Life semantic
  { query: "\u4F60\u8BF4\u8BDD\u4F1A\u5F97\u7F6A\u4EBA\u5417", expectedIndex: 160, type: "semantic", description: "\u5F97\u7F6A\u4EBA\u2192\u76F4\u6765\u76F4\u53BB" },
  { query: "\u4F60\u662F\u7406\u6027\u6D88\u8D39\u8005\u5417", expectedIndex: 162, type: "semantic", description: "\u7406\u6027\u6D88\u8D39\u2192\u505A\u529F\u8BFE\u770B\u6D4B\u8BC4" },
  { query: "\u4F60\u662F\u5185\u5411\u8FD8\u662F\u5916\u5411", expectedIndex: 163, type: "semantic", description: "\u5185\u5411\u5916\u5411\u2192\u4E0D\u559C\u6B22\u5927\u573A\u5408" },
  { query: "\u4F60\u6709\u4EC0\u4E48\u51CF\u538B\u65B9\u5F0F", expectedIndex: 165, type: "semantic", description: "\u51CF\u538B\u2192\u6C5F\u8FB9\u6563\u6B65" },
  { query: "\u4F60\u4E3A\u4EC0\u4E48\u6765\u5317\u4EAC", expectedIndex: 166, type: "semantic", description: "\u6765\u5317\u4EAC\u2192\u5B57\u8282offer" },
  { query: "\u4F60\u53BB\u897F\u5B89\u770B\u4E86\u4EC0\u4E48", expectedIndex: 168, type: "semantic", description: "\u897F\u5B89\u2192\u5175\u9A6C\u4FD1\u5927\u5510\u4E0D\u591C\u57CE" },
  { query: "\u4F60\u72EC\u81EA\u65C5\u884C\u8FC7\u5417", expectedIndex: 170, type: "semantic", description: "\u72EC\u81EA\u65C5\u884C\u2192\u4E91\u5357\u534A\u4E2A\u6708" },
  { query: "\u4F60\u6709\u4EC0\u4E48\u574F\u4E60\u60EF", expectedIndex: [172, 173, 175], type: "semantic", description: "\u574F\u4E60\u60EF\u2192\u9009\u62E9\u56F0\u96BE/\u9759\u97F3/\u66B4\u98DF" },
  { query: "\u4F60\u7684\u604B\u7231\u7ECF\u5386", expectedIndex: [1, 178, 119], type: "semantic", description: "\u604B\u7231\u2192\u5C0F\u96E8/\u524D\u5973\u53CB/\u9886\u8BC1" },
  { query: "\u4F60\u7684\u804C\u4E1A\u8DEF\u5F84", expectedIndex: [179, 86, 0], type: "semantic", description: "\u804C\u4E1A\u8DEF\u5F84\u2192\u7F8E\u56E2\u2192\u5B57\u8282" },
  // Specific details semantic
  { query: "\u4F60\u662F\u82F9\u679C\u751F\u6001\u7684\u7528\u6237\u5417", expectedIndex: [180, 35, 184], type: "semantic", description: "\u82F9\u679C\u2192iPhone/MacBook/AirPods" },
  { query: "\u4F60\u542C\u4EC0\u4E48\u7C7B\u578B\u7684\u97F3\u9891\u5185\u5BB9", expectedIndex: [184, 185], type: "semantic", description: "\u97F3\u9891\u2192\u64AD\u5BA2" },
  { query: "\u4F60\u7684\u7761\u7720\u4E60\u60EF", expectedIndex: [190, 155, 10], type: "semantic", description: "\u7761\u7720\u4E60\u60EF\u2192\u7A7A\u8C03/\u6D17\u6F31/\u5931\u7720" },
  { query: "\u4F60\u505A\u996D\u6709\u4EC0\u4E48\u7279\u70B9", expectedIndex: [193, 48], type: "semantic", description: "\u505A\u996D\u7279\u70B9\u2192\u653E\u849C\u591A/\u7CD6\u918B\u6392\u9AA8" },
  { query: "\u4F60\u548C\u5BB6\u4EBA\u600E\u4E48\u6C9F\u901A", expectedIndex: [194, 112], type: "semantic", description: "\u5BB6\u4EBA\u6C9F\u901A\u2192\u89C6\u9891\u901A\u8BDD/\u50AC\u5A5A" },
  { query: "\u4F60\u5BF9\u6444\u5F71\u611F\u5174\u8DA3\u5417", expectedIndex: [187, 157], type: "semantic", description: "\u6444\u5F71\u2192\u5BCC\u58EB\u76F8\u673A/2\u4E07\u5F20\u7167\u7247" },
  { query: "\u4F60\u6709\u4EC0\u4E48\u53E3\u8154\u95EE\u9898", expectedIndex: 197, type: "semantic", description: "\u53E3\u8154\u2192\u6E83\u75A1\u7F3A\u7EF4B" },
  { query: "\u4F60\u5728\u6298\u817E\u4EC0\u4E48\u6280\u672F\u9879\u76EE", expectedIndex: 198, type: "semantic", description: "\u6280\u672F\u9879\u76EE\u2192Home Assistant" },
  { query: "\u4F60\u5468\u672B\u600E\u4E48\u8FC7", expectedIndex: [199, 148, 30], type: "semantic", description: "\u5468\u672B\u2192\u5B9C\u5BB6/\u770B\u4E66/\u516C\u56ED" },
  { query: "\u4F60\u7A7F\u8863\u6709\u4EC0\u4E48\u4E60\u60EF", expectedIndex: [196, 70], type: "semantic", description: "\u7A7F\u8863\u2192\u7FBD\u7ED2\u670D/\u4F18\u8863\u5E93Zara" },
  // ════════════════════════════════════════════════════════════
  // HARD QUERIES (100 total — 否定/聚合/跨领域/时间推理/抽象)
  // ════════════════════════════════════════════════════════════
  // Negation queries (否定推理)
  { query: "\u4F60\u6709\u4EC0\u4E48\u505A\u4E0D\u5230\u7684\u4E8B", expectedIndex: [75, 47, 172], type: "hard", description: "\u505A\u4E0D\u5230\u2192\u5F00\u8F66/\u5C0F\u63D0\u7434/\u9009\u62E9" },
  { query: "\u4F60\u7684\u5F31\u70B9\u662F\u4EC0\u4E48", expectedIndex: [160, 172, 175], type: "hard", description: "\u5F31\u70B9\u2192\u6025\u8E81/\u9009\u62E9\u56F0\u96BE/\u66B4\u98DF" },
  { query: "\u4F60\u4E0D\u770B\u4EC0\u4E48\u5185\u5BB9", expectedIndex: 78, type: "hard", description: "\u4E0D\u770B\u2192\u5A31\u4E50\u516B\u5366" },
  { query: "\u4F60\u6709\u4EC0\u4E48\u4E0D\u80FD\u5403\u7684", expectedIndex: [51, 120], type: "hard", description: "\u4E0D\u80FD\u5403\u2192\u9999\u83DC/\u4E0D\u80FD\u559D\u9152\u5403\u8FA3" },
  { query: "\u4F60\u6709\u4EC0\u4E48\u4E0D\u6562\u505A\u7684\u4E8B", expectedIndex: [75, 26, 58], type: "hard", description: "\u4E0D\u6562\u2192\u5F00\u8F66/\u86C7/\u6253\u9488" },
  { query: "\u4F60\u653E\u5F03\u8FC7\u4EC0\u4E48", expectedIndex: [47, 135, 156], type: "hard", description: "\u653E\u5F03\u2192\u5C0F\u63D0\u7434/\u8003\u7814/\u5065\u8EAB\u623F" },
  { query: "\u4F60\u540E\u6094\u8FC7\u4EC0\u4E48\u51B3\u5B9A\u5417", expectedIndex: [135, 32], type: "hard", description: "\u540E\u6094\u2192\u8003\u7814/\u7092\u80A1" },
  { query: "\u4F60\u6709\u4EC0\u4E48\u793E\u4EA4\u969C\u788D", expectedIndex: [163, 160], type: "hard", description: "\u793E\u4EA4\u969C\u788D\u2192\u4E0D\u559C\u6B22\u5927\u805A\u4F1A/\u5F97\u7F6A\u4EBA" },
  { query: "\u4F60\u8BA8\u538C\u4EC0\u4E48", expectedIndex: [51, 78, 181], type: "hard", description: "\u8BA8\u538C\u2192\u9999\u83DC/\u516B\u5366/\u88AB\u95EE\u7ED3\u5A5A" },
  { query: "\u4F60\u5931\u8D25\u8FC7\u5417", expectedIndex: [9, 134, 32], type: "hard", description: "\u5931\u8D25\u2192\u9762\u8BD5\u88AB\u5237/\u8003\u7814/\u7092\u80A1" },
  // Aggregation queries (聚合推理)
  { query: "\u4F60\u6BCF\u4E2A\u6708\u7684\u6536\u652F\u662F\u4EC0\u4E48\u6837\u7684", expectedIndex: [139, 11, 68, 127, 128], type: "hard", description: "\u6536\u652F\u2192\u5DE5\u8D44/\u623F\u8D37/\u7F51\u8D2D/\u5B9A\u6295/\u4FDD\u9669" },
  { query: "\u4F60\u8EAB\u4E0A\u6709\u591A\u5C11\u6162\u6027\u75C5", expectedIndex: [120, 124, 123, 2, 197], type: "hard", description: "\u6162\u6027\u75C5\u2192\u80C3\u708E/\u8170\u690E/\u7532\u72B6\u817A/\u8840\u538B/\u6E83\u75A1" },
  { query: "\u4F60\u7684\u6240\u6709\u793E\u4EA4\u5A92\u4F53\u8D26\u53F7", expectedIndex: [40, 41, 42, 43], type: "hard", description: "\u793E\u4EA4\u5A92\u4F53\u2192\u6296\u97F3/\u535A\u5BA2/\u5FAE\u4FE1/\u5C0F\u7EA2\u4E66" },
  { query: "\u4F60\u90FD\u5728\u54EA\u4E9B\u57CE\u5E02\u751F\u6D3B\u8FC7", expectedIndex: [17, 4, 167, 166, 109], type: "hard", description: "\u57CE\u5E02\u2192\u957F\u6C99/\u6B66\u6C49/\u4E0A\u6D77/\u5317\u4EAC" },
  { query: "\u5217\u4E3E\u4F60\u7684\u6240\u6709\u6570\u7801\u8BBE\u5907", expectedIndex: [35, 180, 184, 177], type: "hard", description: "\u6570\u7801\u2192MacBook/iPhone/AirPods/Watch" },
  { query: "\u4F60\u5BB6\u6709\u54EA\u4E9B\u4EBA", expectedIndex: [100, 101, 102, 1, 12], type: "hard", description: "\u5BB6\u4EBA\u2192\u7238/\u5988/\u59B9\u59B9/\u5973\u670B\u53CB/\u5B69\u5B50" },
  { query: "\u4F60\u6709\u54EA\u4E9B\u8FD0\u52A8\u4E60\u60EF", expectedIndex: [6, 20, 14, 36, 176], type: "hard", description: "\u8FD0\u52A8\u2192\u8DD1\u6B65/\u7BEE\u7403/\u7FBD\u6BDB\u7403/\u6F5C\u6C34" },
  { query: "\u4F60\u5728\u591A\u5C11\u4E2A\u516C\u53F8\u5DE5\u4F5C\u8FC7", expectedIndex: [90, 86, 0, 39], type: "hard", description: "\u516C\u53F8\u2192\u767E\u5EA6/\u7F8E\u56E2/\u5B57\u8282" },
  { query: "\u4F60\u5B66\u8FC7\u591A\u5C11\u95E8\u8BED\u8A00", expectedIndex: [96, 7, 33], type: "hard", description: "\u8BED\u8A00\u2192Go/Python/Rust/\u65E5\u8BED" },
  { query: "\u4F60\u7684\u5168\u90E8\u4FDD\u9669\u548C\u7406\u8D22", expectedIndex: [126, 127, 128, 138], type: "hard", description: "\u4FDD\u9669\u7406\u8D22\u2192\u8D27\u57FA/\u5B9A\u6295/\u533B\u7597/\u5B9A\u671F" },
  // Cross-domain queries (跨领域推理)
  { query: "\u5DE5\u4F5C\u538B\u529B\u5BF9\u4F60\u5065\u5EB7\u6709\u5F71\u54CD\u5417", expectedIndex: [19, 124, 10, 55], type: "hard", description: "\u5DE5\u4F5C\u2192\u5065\u5EB7\u2192\u52A0\u73ED/\u8170\u690E/\u5931\u7720/\u4E2D\u6691" },
  { query: "\u4F60\u7684\u7ECF\u6D4E\u72B6\u51B5\u548C\u751F\u6D3B\u8D28\u91CF", expectedIndex: [139, 11, 109, 68], type: "hard", description: "\u7ECF\u6D4E\u751F\u6D3B\u2192\u5DE5\u8D44/\u623F\u8D37/\u623F\u5B50/\u6D88\u8D39" },
  { query: "\u4F60\u7684\u5BB6\u5EAD\u8D23\u4EFB", expectedIndex: [63, 12, 112, 194], type: "hard", description: "\u5BB6\u5EAD\u8D23\u4EFB\u2192\u76D6\u623F/\u6000\u5B55/\u50AC\u5A5A/\u901A\u8BDD" },
  { query: "\u6280\u672F\u80FD\u529B\u5982\u4F55\u5F71\u54CD\u4F60\u7684\u804C\u4E1A", expectedIndex: [96, 98, 145, 93], type: "hard", description: "\u6280\u672F\u2192\u804C\u4E1A\u2192\u7ECF\u9A8C/GitHub/LeetCode/CTO\u8868\u626C" },
  { query: "\u4F60\u7684\u6D88\u8D39\u89C2\u548C\u6536\u5165\u5339\u914D\u5417", expectedIndex: [139, 68, 71, 125], type: "hard", description: "\u6D88\u8D39\u6536\u5165\u2192\u5DE5\u8D44/\u7F51\u8D2D/\u76F2\u76D2/\u6905\u5B50" },
  { query: "\u4F60\u7684\u901A\u52E4\u5F71\u54CD\u4E86\u751F\u6D3B\u8D28\u91CF\u5417", expectedIndex: [72, 73, 150, 19], type: "hard", description: "\u901A\u52E4\u5F71\u54CD\u2192\u5730\u94C1/\u65F6\u95F4/\u6B65\u884C/\u52A0\u73ED" },
  { query: "\u4F60\u7684\u996E\u98DF\u4E60\u60EF\u548C\u5065\u5EB7\u6709\u5173\u7CFB\u5417", expectedIndex: [120, 17, 51, 183], type: "hard", description: "\u996E\u98DF\u5065\u5EB7\u2192\u80C3\u708E/\u5403\u8FA3/\u9999\u83DC/\u5496\u5561" },
  { query: "\u4F60\u7684\u793E\u4EA4\u5708\u90FD\u662F\u4EC0\u4E48\u7C7B\u578B\u7684\u4EBA", expectedIndex: [84, 28, 141, 143], type: "hard", description: "\u793E\u4EA4\u5708\u2192\u540C\u4E8B/\u5BA4\u53CB/\u521B\u4E1A/\u90BB\u5C45" },
  { query: "\u4F60\u7684\u6587\u5316\u751F\u6D3B", expectedIndex: [37, 44, 79, 195], type: "hard", description: "\u6587\u5316\u2192\u4E09\u4F53/\u5468\u6770\u4F26/B\u7AD9/\u9ED1\u5BA2\u4E0E\u753B\u5BB6" },
  { query: "\u4F60\u7684\u7EBF\u4E0A\u548C\u7EBF\u4E0B\u793E\u4EA4", expectedIndex: [42, 142, 14, 36], type: "hard", description: "\u7EBF\u4E0A\u7EBF\u4E0B\u2192\u5FAE\u4FE1/\u72FC\u4EBA\u6740/\u7BEE\u7403/\u7FBD\u6BDB\u7403" },
  // Temporal reasoning (时间推理)
  { query: "\u4F60\u6700\u8FD1\u6362\u4E86\u4EC0\u4E48", expectedIndex: [166, 180, 94], type: "hard", description: "\u6700\u8FD1\u6362\u2192\u642C\u5317\u4EAC/\u6362\u624B\u673A/\u540C\u4E8B\u79BB\u804C" },
  { query: "\u4F60\u53BB\u5E74\u53D1\u751F\u4E86\u4EC0\u4E48\u5927\u4E8B", expectedIndex: [104, 38, 103, 168], type: "hard", description: "\u53BB\u5E74\u2192\u7237\u7237\u8FC7\u4E16/\u8FD1\u89C6\u624B\u672F/\u59B9\u59B9\u7ED3\u5A5A/\u897F\u5B89" },
  { query: "\u4F60\u8FD9\u4E2A\u6708\u8981\u505A\u4EC0\u4E48", expectedIndex: [95, 18, 89], type: "hard", description: "\u8FD9\u4E2A\u6708\u2192\u8FF0\u804C/\u5A5A\u793C/POC" },
  { query: "\u4F60\u660E\u5E74\u6709\u4EC0\u4E48\u8BA1\u5212", expectedIndex: [61, 119, 169], type: "hard", description: "\u660E\u5E74\u2192PMP/\u9886\u8BC1/\u871C\u6708" },
  { query: "\u4F60\u5C0F\u65F6\u5019\u548C\u73B0\u5728\u6709\u4EC0\u4E48\u53D8\u5316", expectedIndex: [56, 57, 166, 0], type: "hard", description: "\u53D8\u5316\u2192\u519C\u6751\u2192\u5317\u4EAC\u2192\u5B57\u8282" },
  { query: "\u4F60\u6700\u8FD1\u4E09\u4E2A\u6708\u505A\u4E86\u4EC0\u4E48", expectedIndex: [89, 93, 94, 146], type: "hard", description: "\u4E09\u4E2A\u6708\u2192POC/CTO/\u540C\u4E8B\u79BB\u804C/\u952E\u76D8" },
  { query: "\u4F60\u7684\u804C\u4E1A\u65F6\u95F4\u7EBF", expectedIndex: [90, 179, 86, 166, 0], type: "hard", description: "\u65F6\u95F4\u7EBF\u2192\u767E\u5EA6\u2192\u7F8E\u56E2\u2192\u5B57\u8282" },
  { query: "\u4F60\u4EC0\u4E48\u65F6\u5019\u5F00\u59CB\u575A\u6301\u7684\u4E60\u60EF", expectedIndex: [6, 25, 127], type: "hard", description: "\u575A\u6301\u2192\u8DD1\u6B65\u4E09\u4E2A\u6708/\u6212\u70DF47\u5929/\u5B9A\u6295" },
  { query: "\u4F60\u8FC7\u53BB\u4E00\u5E74\u7684\u65C5\u884C", expectedIndex: [168, 5, 27], type: "hard", description: "\u65C5\u884C\u2192\u897F\u5B89/\u6210\u90FD/\u65E5\u672C\u8BA1\u5212" },
  { query: "\u4F60\u6700\u8FD1\u7684\u60C5\u611F\u53D8\u5316", expectedIndex: [12, 119, 118], type: "hard", description: "\u60C5\u611F\u2192\u6000\u5B55/\u9886\u8BC1/\u59B9\u59B9\u6000\u5B55" },
  // Abstract / philosophical queries (抽象推理)
  { query: "\u4F60\u7684\u4EBA\u751F\u4F18\u5148\u7EA7", expectedIndex: [12, 63, 60, 62], type: "hard", description: "\u4F18\u5148\u7EA7\u2192\u5BB6\u5EAD/\u7236\u6BCD/\u68A6\u60F3/\u8D22\u52A1" },
  { query: "\u4EC0\u4E48\u5B9A\u4E49\u4E86\u4F60", expectedIndex: [0, 17, 56, 160], type: "hard", description: "\u5B9A\u4E49\u2192\u5DE5\u4F5C/\u5BB6\u4E61/\u7AE5\u5E74/\u6027\u683C" },
  { query: "\u4F60\u6700\u9A84\u50B2\u7684\u4E8B", expectedIndex: [93, 57, 98, 131], type: "hard", description: "\u9A84\u50B2\u2192CTO\u8868\u626C/\u7ADE\u8D5B/GitHub/\u56FD\u5956" },
  { query: "\u4F60\u6700\u5927\u7684\u9057\u61BE", expectedIndex: [134, 47, 59], type: "hard", description: "\u9057\u61BE\u2192\u8003\u7814/\u5C0F\u63D0\u7434/\u65FA\u8D22" },
  { query: "\u4F60\u7684\u5B89\u5168\u611F\u6765\u81EA\u54EA\u91CC", expectedIndex: [1, 128, 109, 139], type: "hard", description: "\u5B89\u5168\u611F\u2192\u5C0F\u96E8/\u4FDD\u9669/\u623F\u5B50/\u5DE5\u8D44" },
  { query: "\u4F60\u5BF9\u81EA\u5DF1\u6EE1\u610F\u5417", expectedIndex: [83, 93, 32, 156], type: "hard", description: "\u6EE1\u610F\u2192\u7EE9\u6548B+/\u88AB\u8868\u626C/\u4E8F\u94B1/\u5065\u8EAB\u653E\u5F03" },
  { query: "\u4F60\u5728\u9003\u907F\u4EC0\u4E48", expectedIndex: [112, 163, 75], type: "hard", description: "\u9003\u907F\u2192\u50AC\u5A5A/\u793E\u4EA4/\u5F00\u8F66" },
  { query: "\u4F60\u7684\u7CBE\u795E\u4E16\u754C", expectedIndex: [37, 44, 79, 60], type: "hard", description: "\u7CBE\u795E\u2192\u4E09\u4F53/\u5468\u6770\u4F26/B\u7AD9/\u5496\u5561\u5E97\u68A6" },
  { query: "\u4F60\u7684\u7126\u8651\u6765\u6E90", expectedIndex: [19, 11, 31, 95], type: "hard", description: "\u7126\u8651\u2192\u52A0\u73ED/\u623F\u8D37/\u6362\u5DE5\u4F5C/\u664B\u5347" },
  { query: "\u4F60\u7684\u5E78\u798F\u65F6\u523B", expectedIndex: [12, 8, 5, 177], type: "hard", description: "\u5E78\u798F\u2192\u6000\u5B55/\u5988\u5988\u7EA2\u70E7\u8089/\u6210\u90FD/\u751F\u65E5\u793C\u7269" },
  // Paraphrase / synonym queries (同义改写)
  { query: "\u4F60\u7684\u4EE3\u6B65\u5DE5\u5177", expectedIndex: [22, 72, 74], type: "hard", description: "\u4EE3\u6B65\u2192\u7279\u65AF\u62C9/\u5730\u94C1/\u5355\u8F66" },
  { query: "\u4F60\u5403\u4EC0\u4E48\u4FDD\u5065\u54C1", expectedIndex: 122, type: "hard", description: "\u4FDD\u5065\u54C1\u2192\u836F\uFF08\u6A21\u7CCA\u8FB9\u754C\uFF09" },
  { query: "\u4F60\u6709\u4EC0\u4E48\u8BC1\u4E66", expectedIndex: [75, 176, 61], type: "hard", description: "\u8BC1\u4E66\u2192\u9A7E\u7167/PADI OW/PMP\u8BA1\u5212" },
  { query: "\u4F60\u5199\u8FC7\u591A\u5C11\u4EE3\u7801", expectedIndex: [41, 98, 145], type: "hard", description: "\u4EE3\u7801\u2192\u535A\u5BA2/GitHub/LeetCode" },
  { query: "\u4F60\u7684\u5C45\u4F4F\u73AF\u5883", expectedIndex: [109, 143, 116], type: "hard", description: "\u5C45\u4F4F\u2192\u56DE\u9F99\u89C2/\u90BB\u5C45/\u91D1\u9C7C\u7EFF\u841D" },
  { query: "\u4F60\u7684\u5A31\u4E50\u5F00\u652F", expectedIndex: [71, 147, 146], type: "hard", description: "\u5A31\u4E50\u5F00\u652F\u2192\u76F2\u76D2/\u539F\u795E/\u952E\u76D8" },
  { query: "\u4F60\u7684\u5C4F\u5E55\u65F6\u95F4", expectedIndex: [40, 66, 67], type: "hard", description: "\u5C4F\u5E55\u65F6\u95F4\u2192\u6296\u97F3/B\u7AD9/\u5FAE\u535A" },
  { query: "\u4F60\u7684\u4E0A\u4E0B\u73ED\u8DEF\u7EBF", expectedIndex: [72, 150, 74], type: "hard", description: "\u8DEF\u7EBF\u2192\u5730\u94C1/\u8D70\u8DEF15\u5206/\u5355\u8F66" },
  { query: "\u4F60\u7684\u5B66\u5386\u80CC\u666F", expectedIndex: [4, 131, 136], type: "hard", description: "\u5B66\u5386\u2192\u6B66\u6C49/\u6B66\u5927/\u957F\u6C99\u4E00\u4E2D" },
  { query: "\u4F60\u7684\u526F\u4E1A", expectedIndex: [41, 98], type: "hard", description: "\u526F\u4E1A\u2192\u6280\u672F\u535A\u5BA2/\u5F00\u6E90\u9879\u76EE" },
  // Complex scenario queries (复杂场景)
  { query: "\u5982\u679C\u4F60\u751F\u75C5\u4E86\u8C01\u7167\u987E\u4F60", expectedIndex: [1, 101, 102], type: "hard", description: "\u7167\u987E\u2192\u5C0F\u96E8/\u5988\u5988/\u59B9\u59B9" },
  { query: "\u4F60\u9000\u4F11\u540E\u4F1A\u505A\u4EC0\u4E48", expectedIndex: [60, 117, 187], type: "hard", description: "\u9000\u4F11\u2192\u5496\u5561\u5E97/\u50CF\u7238\u9493\u9C7C/\u6444\u5F71" },
  { query: "\u4F60\u7684\u5B69\u5B50\u51FA\u751F\u540E\u751F\u6D3B\u4F1A\u600E\u4E48\u53D8", expectedIndex: [12, 109, 139, 19], type: "hard", description: "\u5B69\u5B50\u51FA\u751F\u2192\u9884\u4EA7\u671F/\u623F\u5B50/\u5DE5\u8D44/\u52A0\u73ED" },
  { query: "\u642C\u5230\u5317\u4EAC\u540E\u4F60\u5931\u53BB\u4E86\u4EC0\u4E48", expectedIndex: [167, 106, 100], type: "hard", description: "\u5931\u53BB\u2192\u4E0A\u6D77\u751F\u6D3B/\u79BB\u5BB6\u8FDC/\u79BB\u7236\u6BCD\u8FDC" },
  { query: "\u4F60\u89C9\u5F97\u81EA\u5DF1\u5065\u5EB7\u5417", expectedIndex: [120, 124, 10, 2, 197], type: "hard", description: "\u5065\u5EB7\u2192\u80C3\u708E/\u8170\u690E/\u5931\u7720/\u8840\u538B/\u6E83\u75A1" },
  { query: "\u4F60\u6700\u82B1\u94B1\u7684\u662F\u4EC0\u4E48", expectedIndex: [11, 125, 109], type: "hard", description: "\u82B1\u94B1\u2192\u623F\u8D37/\u6905\u5B50/\u623F\u5B50" },
  { query: "\u4F60\u7684\u793E\u4F1A\u5173\u7CFB\u7F51", expectedIndex: [84, 28, 82, 141, 143], type: "hard", description: "\u5173\u7CFB\u7F51\u2192\u674E\u6668/\u5F20\u78CA/leader/\u5218\u6BC5/\u90BB\u5C45" },
  { query: "\u4F60\u7684\u4FE1\u606F\u83B7\u53D6\u6E20\u9053", expectedIndex: [76, 79, 185, 43], type: "hard", description: "\u4FE1\u606F\u219236kr/B\u7AD9/\u64AD\u5BA2/\u5C0F\u7EA2\u4E66" },
  { query: "\u4F60\u4EBA\u751F\u7684\u8F6C\u6298\u70B9", expectedIndex: [166, 134, 178, 0], type: "hard", description: "\u8F6C\u6298\u2192\u642C\u5317\u4EAC/\u8003\u7814\u5931\u8D25/\u5206\u624B/\u5B57\u8282offer" },
  { query: "\u4F60\u4ECE\u7236\u6BCD\u8EAB\u4E0A\u7EE7\u627F\u4E86\u4EC0\u4E48", expectedIndex: [100, 17, 107, 2], type: "hard", description: "\u7EE7\u627F\u2192\u6570\u5B66/\u6E56\u5357/\u9AD8\u8840\u538B\u9057\u4F20" },
  // ════════════════════════════════════════════════════════════
  // ADDITIONAL SEMANTIC QUERIES (filling to 200 semantic)
  // ════════════════════════════════════════════════════════════
  { query: "\u4F60\u4E0B\u5348\u72AF\u56F0\u600E\u4E48\u529E", expectedIndex: 152, type: "semantic", description: "\u72AF\u56F0\u2192\u5496\u5561\u7EED\u547D" },
  { query: "\u4F60\u6700\u5E38\u5403\u7684\u5916\u5356\u662F\u4EC0\u4E48", expectedIndex: 153, type: "semantic", description: "\u5E38\u5403\u2192\u9EC4\u7116\u9E21" },
  { query: "\u4F60\u6709\u6D01\u7656\u5417", expectedIndex: [154, 192], type: "semantic", description: "\u6D01\u7656\u2192\u5439\u5E72\u5934\u53D1/\u786E\u8BA4\u9501\u95E8" },
  { query: "\u4F60\u51E0\u70B9\u4E0A\u5E8A", expectedIndex: 155, type: "semantic", description: "\u4E0A\u5E8A\u2192\u5341\u70B9\u534A\u6D17\u6F31" },
  { query: "\u4F60\u529E\u4E86\u4EC0\u4E48\u4F1A\u5458\u5361", expectedIndex: 156, type: "semantic", description: "\u4F1A\u5458\u5361\u2192\u5065\u8EAB\u623F\u5E74\u5361" },
  { query: "\u4F60\u7528\u4EC0\u4E48\u8BB0\u5F55\u751F\u6D3B", expectedIndex: [157, 158], type: "semantic", description: "\u8BB0\u5F55\u2192\u62CD\u7167/Notion" },
  { query: "\u4F60\u548C\u5973\u670B\u53CB\u7684\u7EA6\u4F1A\u6D3B\u52A8", expectedIndex: [159, 199], type: "semantic", description: "\u7EA6\u4F1A\u2192\u770B\u7EFC\u827A/\u901B\u5B9C\u5BB6" },
  { query: "\u4F60\u6027\u683C\u4E0A\u5BB9\u6613\u5403\u4E8F\u5417", expectedIndex: [160, 174], type: "semantic", description: "\u5403\u4E8F\u2192\u76F4\u6765\u76F4\u53BB/\u4E0D\u6C42\u4EBA" },
  { query: "\u4F60\u662F\u5B8C\u7F8E\u4E3B\u4E49\u8005\u5417", expectedIndex: [162, 164, 192], type: "semantic", description: "\u5B8C\u7F8E\u4E3B\u4E49\u2192\u6D4B\u8BC4/\u6E05\u5355/\u5F3A\u8FEB\u75C7" },
  { query: "\u4F60\u7684\u6563\u6B65\u4E60\u60EF", expectedIndex: [165, 150], type: "semantic", description: "\u6563\u6B65\u2192\u6C5F\u8FB9/\u8D70\u8DEF\u53BB\u5730\u94C1" },
  { query: "\u4F60\u4F4F\u8FC7\u51E0\u4E2A\u57CE\u5E02", expectedIndex: [17, 4, 167, 109], type: "semantic", description: "\u4F4F\u8FC7\u2192\u957F\u6C99/\u6B66\u6C49/\u4E0A\u6D77/\u5317\u4EAC" },
  { query: "\u4F60\u56FD\u5E86\u4E00\u822C\u600E\u4E48\u5B89\u6392", expectedIndex: [168, 5], type: "semantic", description: "\u56FD\u5E86\u2192\u897F\u5B89/\u6210\u90FD" },
  { query: "\u4F60\u6709\u4EC0\u4E48\u6781\u9650\u8FD0\u52A8\u7ECF\u5386", expectedIndex: 176, type: "semantic", description: "\u6781\u9650\u8FD0\u52A8\u2192\u6F5C\u6C34" },
  { query: "\u4F60\u6536\u5230\u8FC7\u4EC0\u4E48\u5370\u8C61\u6DF1\u523B\u7684\u793C\u7269", expectedIndex: [177, 99], type: "semantic", description: "\u793C\u7269\u2192Apple Watch/iPad Pro" },
  { query: "\u4F60\u4E4B\u524D\u7684\u611F\u60C5\u7ECF\u5386", expectedIndex: 178, type: "semantic", description: "\u4E4B\u524D\u611F\u60C5\u2192\u524D\u5973\u53CB\u5F02\u5730" },
  { query: "\u4F60\u4ECE\u5B9E\u4E60\u5230\u73B0\u5728\u591A\u4E45\u4E86", expectedIndex: [90, 179], type: "semantic", description: "\u5B9E\u4E60\u81F3\u4ECA\u2192\u767E\u5EA6\u5B9E\u4E60/\u7F8E\u56E2\u8F6C\u6B63" },
  { query: "\u4F60\u4EE5\u524D\u7528\u5B89\u5353\u5417", expectedIndex: 180, type: "semantic", description: "\u5B89\u5353\u2192\u4E4B\u524D\u4E00\u76F4\u7528" },
  { query: "\u4F60\u4E3A\u4EC0\u4E48\u4E0D\u7528\u7F51\u6613\u4E91", expectedIndex: 182, type: "semantic", description: "\u4E0D\u7528\u7F51\u6613\u4E91\u2192\u7248\u6743\u5C11" },
  { query: "\u4F60\u559D\u5496\u5561\u52A0\u7CD6\u5417", expectedIndex: 183, type: "semantic", description: "\u52A0\u7CD6\u2192\u4E0D\u52A0\u7CD6\u4E0D\u52A0\u5976" },
  { query: "\u4F60\u901A\u52E4\u8DEF\u4E0A\u505A\u4EC0\u4E48", expectedIndex: [184, 185], type: "semantic", description: "\u901A\u52E4\u8DEF\u4E0A\u2192\u542C\u64AD\u5BA2" },
  { query: "\u4F60\u6709\u9605\u8BFB\u4E60\u60EF\u5417", expectedIndex: [186, 148, 37], type: "semantic", description: "\u9605\u8BFB\u2192\u4E70\u4E66/\u5496\u5561\u9986\u770B\u4E66/\u4E09\u4F53" },
  { query: "\u4F60\u6709\u4EC0\u4E48\u60F3\u5165\u624B\u7684\u65B0\u88C5\u5907", expectedIndex: [187, 16], type: "semantic", description: "\u65B0\u88C5\u5907\u2192\u5BCC\u58EB\u76F8\u673A/\u7279\u65AF\u62C9" },
  { query: "\u4F60\u642C\u8FC7\u5BB6\u5417", expectedIndex: [188, 166], type: "semantic", description: "\u642C\u5BB6\u2192\u6254\u4E1C\u897F/\u4E0A\u6D77\u5230\u5317\u4EAC" },
  { query: "\u4F60\u7761\u89C9\u6709\u4EC0\u4E48\u8BB2\u7A76", expectedIndex: [190, 10], type: "semantic", description: "\u7761\u89C9\u8BB2\u7A76\u2192\u7A7A\u8C03/\u5931\u7720" },
  { query: "\u4F60\u51FA\u95E8\u524D\u6709\u4EC0\u4E48\u4EEA\u5F0F", expectedIndex: 192, type: "semantic", description: "\u51FA\u95E8\u4EEA\u5F0F\u2192\u786E\u8BA4\u9501\u95E8" },
  { query: "\u4F60\u505A\u996D\u53E3\u5473\u91CD\u5417", expectedIndex: [193, 17], type: "semantic", description: "\u53E3\u5473\u91CD\u2192\u653E\u849C\u591A/\u80FD\u5403\u8FA3" },
  { query: "\u4F60\u548C\u7236\u6BCD\u611F\u60C5\u597D\u5417", expectedIndex: [194, 63, 112], type: "semantic", description: "\u7236\u6BCD\u611F\u60C5\u2192\u901A\u8BDD/\u76D6\u623F/\u50AC\u5A5A" },
  { query: "\u4F60\u6709\u4EC0\u4E48\u9605\u8BFB\u63A8\u8350", expectedIndex: [195, 37], type: "semantic", description: "\u63A8\u8350\u2192\u9ED1\u5BA2\u4E0E\u753B\u5BB6/\u4E09\u4F53" },
  { query: "\u4F60\u6015\u70ED\u8FD8\u662F\u6015\u51B7", expectedIndex: [52, 55], type: "semantic", description: "\u6015\u70ED\u51B7\u2192\u6015\u51B7/\u4E2D\u6691" },
  { query: "\u4F60\u7259\u9F7F\u6709\u4EC0\u4E48\u95EE\u9898", expectedIndex: 197, type: "semantic", description: "\u7259\u9F7F\u2192\u53E3\u8154\u6E83\u75A1" },
  { query: "\u4F60\u5BB6\u6709\u4EC0\u4E48\u667A\u80FD\u8BBE\u5907", expectedIndex: 198, type: "semantic", description: "\u667A\u80FD\u8BBE\u5907\u2192Home Assistant" },
  { query: "\u4F60\u901B\u8857\u4E00\u822C\u53BB\u54EA", expectedIndex: [199, 70], type: "semantic", description: "\u901B\u8857\u2192\u5B9C\u5BB6/\u4F18\u8863\u5E93Zara" },
  { query: "\u4F60\u7684\u5496\u5561\u56E0\u6444\u5165", expectedIndex: [64, 152, 91, 183], type: "semantic", description: "\u5496\u5561\u56E0\u2192\u65E9\u4E0A\u5496\u5561/\u4E0B\u5348\u5496\u5561/\u661F\u5DF4\u514B/\u7F8E\u5F0F" },
  { query: "\u4F60\u7684\u5DE5\u4F5C\u73AF\u5883\u600E\u4E48\u6837", expectedIndex: [92, 85, 91], type: "semantic", description: "\u5DE5\u4F5C\u73AF\u5883\u2192\u964D\u566A/\u663E\u793A\u5668/\u661F\u5DF4\u514B" },
  { query: "\u4F60\u6709\u4EC0\u4E48\u7ADE\u8D5B\u7ECF\u5386", expectedIndex: [57, 144], type: "semantic", description: "\u7ADE\u8D5B\u2192\u6570\u5B66\u7ADE\u8D5B/\u9ED1\u5BA2\u9A6C\u62C9\u677E" },
  // ════════════════════════════════════════════════════════════
  // ADDITIONAL HARD QUERIES (filling to 100 hard)
  // ════════════════════════════════════════════════════════════
  { query: "\u4F60\u540C\u65F6\u5728\u5B66\u51E0\u6837\u4E1C\u897F", expectedIndex: [7, 33, 89, 198], type: "hard", description: "\u540C\u65F6\u5B66\u2192Rust/\u65E5\u8BED/XGBoost/HA" },
  { query: "\u4F60\u7684\u5F00\u9500\u6BD4\u6536\u5165\u5927\u5417", expectedIndex: [139, 11, 68, 71], type: "hard", description: "\u5F00\u9500\u6536\u5165\u2192\u5DE5\u8D44vs\u623F\u8D37/\u7F51\u8D2D/\u76F2\u76D2" },
  { query: "\u4F60\u8EAB\u8FB9\u8C01\u6700\u8FD1\u6709\u53D8\u52A8", expectedIndex: [94, 118, 114], type: "hard", description: "\u53D8\u52A8\u2192\u5C0F\u9648\u79BB\u804C/\u59B9\u59B9\u6000\u5B55/\u8868\u5F1F\u9AD8\u8003" },
  { query: "\u63CF\u8FF0\u4F60\u7684\u65E9\u6668", expectedIndex: [149, 20, 64, 150, 72], type: "hard", description: "\u65E9\u6668\u2192\u95F9\u949F/\u8DD1\u6B65/\u5496\u5561/\u8D70\u8DEF/\u5730\u94C1" },
  { query: "\u4F60\u7684\u4EBA\u9645\u5173\u7CFB\u6709\u4EC0\u4E48\u51B2\u7A81", expectedIndex: [160, 82, 112], type: "hard", description: "\u51B2\u7A81\u2192\u813E\u6C14/leader\u8981\u6C42\u9AD8/\u50AC\u5A5A" },
  { query: "\u4F60\u82B1\u5728\u5C4F\u5E55\u4E0A\u7684\u603B\u65F6\u95F4", expectedIndex: [40, 66, 67, 147], type: "hard", description: "\u5C4F\u5E55\u603B\u65F6\u95F4\u2192\u6296\u97F3/B\u7AD9/\u5FAE\u535A/\u539F\u795E" },
  { query: "\u4F60\u7684\u623F\u5B50\u76F8\u5173\u5F00\u652F", expectedIndex: [11, 130, 109], type: "hard", description: "\u623F\u5B50\u5F00\u652F\u2192\u623F\u8D37/\u516C\u79EF\u91D1/\u4E70\u623F" },
  { query: "\u4F60\u5728\u4E0D\u540C\u57CE\u5E02\u7684\u7ECF\u5386", expectedIndex: [17, 4, 167, 166, 171], type: "hard", description: "\u57CE\u5E02\u7ECF\u5386\u2192\u957F\u6C99/\u6B66\u6C49/\u4E0A\u6D77/\u5317\u4EAC/\u51FA\u5DEE" },
  { query: "\u4F60\u7684\u6240\u6709\u6050\u60E7\u548C\u7126\u8651", expectedIndex: [26, 58, 52, 19, 95], type: "hard", description: "\u6050\u60E7\u7126\u8651\u2192\u86C7/\u6253\u9488/\u51B7/\u52A0\u73ED/\u664B\u5347" },
  { query: "\u5F71\u54CD\u4F60\u4EBA\u751F\u8F68\u8FF9\u7684\u4EBA", expectedIndex: [100, 136, 82, 1], type: "hard", description: "\u5F71\u54CD\u4EBA\u2192\u7238/\u73ED\u4E3B\u4EFB\u5218/leader/\u5C0F\u96E8" },
  { query: "\u4F60\u7684\u957F\u671F\u6295\u8D44\u6709\u54EA\u4E9B", expectedIndex: [127, 126, 138, 128], type: "hard", description: "\u957F\u671F\u6295\u8D44\u2192\u5B9A\u6295/\u8D27\u57FA/\u5B9A\u671F/\u4FDD\u9669" },
  { query: "\u4F60\u7684\u6240\u6709\u4E0D\u826F\u4E60\u60EF", expectedIndex: [40, 175, 172, 156, 10], type: "hard", description: "\u4E0D\u826F\u2192\u6296\u97F3/\u66B4\u98DF/\u9009\u62E9\u56F0\u96BE/\u4E0D\u5065\u8EAB/\u5931\u7720" },
  { query: "\u4F60\u62E5\u6709\u7684\u6240\u6709\u8BC1\u4E66\u548C\u8D44\u8D28", expectedIndex: [75, 176], type: "hard", description: "\u8BC1\u4E66\u8D44\u8D28\u2192\u9A7E\u7167/PADI OW" },
  { query: "\u4F60\u6700\u4EB2\u8FD1\u7684\u4E94\u4E2A\u4EBA", expectedIndex: [1, 100, 101, 102, 84], type: "hard", description: "\u4EB2\u8FD1\u2192\u5C0F\u96E8/\u7238/\u5988/\u59B9\u59B9/\u674E\u6668" },
  { query: "\u4F60\u8FD9\u8F88\u5B50\u642C\u4E86\u51E0\u6B21\u5BB6", expectedIndex: [56, 4, 167, 166, 188], type: "hard", description: "\u642C\u5BB6\u2192\u519C\u6751/\u6B66\u6C49/\u4E0A\u6D77/\u5317\u4EAC/\u6254\u4E1C\u897F" },
  { query: "\u4F60\u4E00\u5929\u559D\u51E0\u676F\u5496\u5561", expectedIndex: [64, 152, 91], type: "hard", description: "\u5496\u5561\u6B21\u6570\u2192\u65E9\u4E0A/\u4E0B\u5348/\u661F\u5DF4\u514B" },
  { query: "\u4F60\u5BF9\u5B57\u8282\u7684\u6574\u4F53\u8BC4\u4EF7", expectedIndex: [97, 92, 93, 19], type: "hard", description: "\u5B57\u8282\u8BC4\u4EF7\u2192\u798F\u5229/\u566A\u97F3/\u88AB\u8868\u626C/\u52A0\u73ED" },
  { query: "\u4F60\u8FD9\u51E0\u5E74\u9519\u8FC7\u4E86\u4EC0\u4E48", expectedIndex: [134, 47, 156, 32], type: "hard", description: "\u9519\u8FC7\u2192\u8003\u7814/\u5C0F\u63D0\u7434/\u5065\u8EAB/\u7092\u80A1" },
  { query: "\u4F60\u73B0\u5728\u6700\u62C5\u5FC3\u4EC0\u4E48", expectedIndex: [12, 95, 120, 19], type: "hard", description: "\u62C5\u5FC3\u2192\u6000\u5B55/\u664B\u5347/\u80C3\u708E/\u52A0\u73ED" },
  { query: "\u4F60\u548C\u5C0F\u96E8\u7684\u672A\u6765\u89C4\u5212", expectedIndex: [119, 169, 12, 109], type: "hard", description: "\u672A\u6765\u2192\u9886\u8BC1/\u871C\u6708/\u5B69\u5B50/\u623F\u5B50" },
  { query: "\u4F60\u51CF\u8F7B\u5DE5\u4F5C\u75B2\u52B3\u7684\u65B9\u5F0F", expectedIndex: [45, 152, 91, 165], type: "hard", description: "\u51CF\u75B2\u52B3\u2192lo-fi/\u5496\u5561/\u661F\u5DF4\u514B/\u6563\u6B65" },
  { query: "\u4F60\u751F\u6D3B\u4E2D\u7684\u4EEA\u5F0F\u611F", expectedIndex: [64, 192, 155, 194], type: "hard", description: "\u4EEA\u5F0F\u2192\u5496\u5561/\u9501\u95E8/\u6D17\u6F31/\u89C6\u9891\u901A\u8BDD" },
  { query: "\u4F60\u7684\u77E5\u8BC6\u4F53\u7CFB", expectedIndex: [96, 145, 41, 158], type: "hard", description: "\u77E5\u8BC6\u2192\u6280\u672F\u6808/LeetCode/\u535A\u5BA2/Notion" },
  { query: "\u4F60\u548C\u5BB6\u4EBA\u7684\u8DDD\u79BB", expectedIndex: [17, 109, 166, 194], type: "hard", description: "\u8DDD\u79BB\u2192\u957F\u6C99/\u5317\u4EAC/\u642C\u5BB6/\u901A\u8BDD" },
  { query: "\u4F60\u751F\u6D3B\u4E2D\u7684\u77DB\u76FE", expectedIndex: [120, 17, 19, 156], type: "hard", description: "\u77DB\u76FE\u2192\u80C3\u708E\u4F46\u5403\u8FA3/\u52A0\u73ED\u7D2F/\u4E0D\u5065\u8EAB" },
  { query: "\u4F60\u7684\u788E\u7247\u65F6\u95F4\u90FD\u5728\u505A\u4EC0\u4E48", expectedIndex: [40, 67, 66, 184], type: "hard", description: "\u788E\u7247\u2192\u6296\u97F3/\u5FAE\u535A/B\u7AD9/\u64AD\u5BA2" },
  { query: "\u4F60\u6709\u54EA\u4E9B\u5B9A\u671F\u8981\u505A\u7684\u4E8B", expectedIndex: [121, 127, 194, 36], type: "hard", description: "\u5B9A\u671F\u2192\u80C3\u955C/\u5B9A\u6295/\u901A\u8BDD/\u7FBD\u6BDB\u7403" },
  { query: "\u4F60\u7684\u98DF\u7269\u5730\u56FE", expectedIndex: [17, 5, 48, 153, 51], type: "hard", description: "\u98DF\u7269\u2192\u8FA3/\u706B\u9505/\u7CD6\u918B\u6392\u9AA8/\u9EC4\u7116\u9E21/\u9999\u83DC" },
  { query: "\u4F60\u7684\u82F9\u679C\u5168\u5BB6\u6876", expectedIndex: [180, 35, 184, 177], type: "hard", description: "\u82F9\u679C\u2192iPhone/MacBook/AirPods/Watch" },
  { query: "\u603B\u7ED3\u4F60\u7684\u6027\u683C", expectedIndex: [160, 161, 163, 174, 172], type: "hard", description: "\u6027\u683C\u2192\u6025\u8E81/\u6B63\u4E49/\u5185\u5411/\u72EC\u7ACB/\u7EA0\u7ED3" }
];
function runBenchmark() {
  console.log("\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550");
  console.log("  cc-soul \u65E0\u5411\u91CF\u53EC\u56DE\u57FA\u51C6\u6D4B\u8BD5");
  console.log("\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550");
  console.log();
  for (const mem of TEST_MEMORIES) {
    learnAssociation(mem.content, 0.3);
  }
  try {
    const factStore = require2("./fact-store.ts");
    for (const mem of TEST_MEMORIES) {
      factStore.extractAndStoreFacts?.(mem.content, "user");
    }
  } catch {
  }
  let directHits = 0, directTotal = 0;
  let semanticHits = 0, semanticTotal = 0;
  let hardHits = 0, hardTotal = 0;
  let top1Hits = 0;
  const failures = [];
  for (const tc of TEST_CASES) {
    const results = activationRecall(TEST_MEMORIES, tc.query, 3, 0, 0.5);
    const resultContents = results.map((r) => r.content);
    const indices = Array.isArray(tc.expectedIndex) ? tc.expectedIndex : [tc.expectedIndex];
    const expectedContents = indices.map((i) => TEST_MEMORIES[i].content);
    const hit = expectedContents.some((ec) => resultContents.includes(ec));
    const isTop1 = expectedContents.some((ec) => resultContents[0] === ec);
    if (tc.type === "direct") {
      directTotal++;
      if (hit) directHits++;
    } else if (tc.type === "semantic") {
      semanticTotal++;
      if (hit) semanticHits++;
    } else {
      hardTotal++;
      if (hit) hardHits++;
    }
    if (isTop1) top1Hits++;
    if (!hit) {
      failures.push({
        query: tc.query,
        type: tc.type,
        desc: tc.description,
        got: resultContents.map((c) => c.slice(0, 30))
      });
    }
    const mark = hit ? isTop1 ? "\u2705" : "\u{1F7E1}" : "\u274C";
    console.log(`${mark} [${tc.type.padEnd(8)}] ${tc.description.padEnd(20)} | ${tc.query}`);
  }
  const allHits = directHits + semanticHits + hardHits;
  const allTotal = directTotal + semanticTotal + hardTotal;
  console.log();
  console.log("\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550");
  console.log("  \u7ED3\u679C\u6C47\u603B");
  console.log("\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550");
  console.log();
  const directRate = (directHits / directTotal * 100).toFixed(0);
  const semanticRate = (semanticHits / semanticTotal * 100).toFixed(0);
  const hardRate = (hardHits / hardTotal * 100).toFixed(0);
  const totalRate = (allHits / allTotal * 100).toFixed(0);
  const top1Rate = (top1Hits / allTotal * 100).toFixed(0);
  console.log(`  \u76F4\u63A5\u53EC\u56DE (top-3):  ${directHits}/${directTotal} = ${directRate}%`);
  console.log(`  \u8BED\u4E49\u53EC\u56DE (top-3):  ${semanticHits}/${semanticTotal} = ${semanticRate}%`);
  console.log(`  \u56F0\u96BE\u53EC\u56DE (top-3):  ${hardHits}/${hardTotal} = ${hardRate}%`);
  console.log(`  \u603B\u4F53 (top-3):      ${allHits}/${allTotal} = ${totalRate}%`);
  console.log(`  Top-1 \u51C6\u786E\u7387:      ${top1Hits}/${allTotal} = ${top1Rate}%`);
  console.log();
  if (failures.length > 0) {
    console.log("  \u2500\u2500 \u5931\u8D25\u7528\u4F8B \u2500\u2500");
    for (const f of failures) {
      console.log(`  \u274C [${f.type}] ${f.desc}: "${f.query}"`);
      console.log(`     \u5B9E\u9645\u8FD4\u56DE: ${f.got.join(" | ")}`);
    }
  }
}
runBenchmark();

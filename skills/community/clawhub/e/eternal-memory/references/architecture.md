# Eternal Memory 架构白皮书

## 设计哲学
- **追加不修改**: 所有原始材料永久保存在L1a，SHA256确保不可篡改
- **校验优于信任**: L1c哈希+语义+拓扑三重验证，失败自动降级
- **零云依赖**: 纯本地TF-IDF向量引擎，零API key，零网络

## L1c校验机制
1. 字面子串匹配（O(n)，最快）
2. 关键词匹配（75%阈值）
3. 窗口Jaccard（降级）
4. 向量相似度（仅长文本，ONNX可用时）

## 拓扑评分公式
importance = 0.35·recency + 0.25·citation + 0.20·connectivity + 0.10·size + 0.10·type

## 降级自愈
FTS5→图谱→Jaccard→归档→rebuild-index（4阶段链）

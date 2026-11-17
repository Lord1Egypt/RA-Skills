> **V7 兼容性说明**：本文件从 V6 完整继承。V7 保留所有 V6 能力，本文件内容完全有效。
> V7 新增 references 见 `references/edge-cloud-architecture.md` / `references/zero-upload-privacy.md` / `references/npu-scheduling-guide.md` / `references/edge-cloud-protocol.md` / `references/audit-report-v7.md`。
> 原始文件版本：V6 · 继承版本：V7 · 继承日期：2026-08-15

# 五大生产力场景详细指南

> 对应第三期大赛五个推荐方向，每个场景包含完整的工具链、教学流程、产出规格和评分映射。

## 场景一：办公提效

### 场景描述
教师日常办公中的重复性任务自动化：文档处理、邮件撰写、会议纪要、通知发布、课表管理等。

### 工具链配置
```
OCR (port:8901) → 文档扫描数字化
TTS (port:8903) → 语音通知合成
RAG (port:8904) → 规章制度知识库
Gateway (port:8900) → 流程编排
```

### 教学应用流程

#### 1. 试卷/教材数字化（OCR）
```javascript
// p5.js 中调用 OCR 服务
async function digitizeExamPaper(imageFile) {
  const result = await fetch('http://localhost:8901/recognize', {
    method: 'POST',
    body: JSON.stringify({
      image: await fileToBase64(imageFile),
      output_format: 'structured',  // 结构化输出
      detect_table: true,           // 表格识别
      detect_formula: true          // 公式识别
    })
  });
  const data = await result.json();
  return {
    text: data.structured_text,
    tables: data.tables,
    formulas: data.formulas,
    confidence: data.confidence
  };
}
```

#### 2. 智能通知合成（TTS）
```javascript
async function generateVoiceNotice(text, voice = 'xiaoyun') {
  const result = await fetch('http://localhost:8903/synthesize', {
    method: 'POST',
    body: JSON.stringify({
      text: text,
      voice: voice,
      speed: 1.0,
      output_format: 'mp3'
    })
  });
  return result.json(); // { audio_url, duration }
}
```

#### 3. 制度问答（RAG）
```javascript
async function queryPolicy(question) {
  const result = await fetch('http://localhost:8904/query', {
    method: 'POST',
    body: JSON.stringify({
      query: question,
      top_k: 3,
      collection: 'school_policies'
    })
  });
  return result.json(); // { answer, sources, confidence }
}
```

### 产出规格
| 产出物 | 格式 | 质量标准 |
|--------|------|----------|
| 数字化试卷 | Markdown/PDF | OCR 准确率 ≥95%，表格完整还原 |
| 语音通知 | MP3/WAV | 发音准确，语速适中，≤30秒 |
| 制度问答 | JSON | 答案准确率 ≥90%，引用来源 |
| 自动化流程 | HTML 演示 | 展示前后对比，效率提升量化 |

### 评分映射
- **场景价值(30%)**: 解决教师高频痛点，日均节省 30+ 分钟
- **商用生产力(30%)**: 可部署为学校办公自动化方案
- **工具使用(20%)**: OCR + TTS + RAG 三工具联动

---

## 场景二：知识管理

### 场景描述
教学资源的知识化管理：课件索引、知识点图谱、教学资料检索、个人知识体系构建。

### 工具链配置
```
OCR (port:8901) → 纸质资料数字化
RAG (port:8904) → 教学知识库构建
Analysis (port:8905) → 知识图谱可视化
Gateway (port:8900) → 知识流水线
```

### 教学应用流程

#### 1. 教学资料数字化入库
```javascript
async function buildKnowledgeBase(materials) {
  const pipeline = new TeachingPipeline('http://localhost:8900');
  
  const results = [];
  for (const material of materials) {
    // Step 1: OCR 识别
    const ocrResult = await pipeline.ocrRecognize(material.image);
    // Step 2: 知识提取与入库
    const ragResult = await pipeline.ragIngest(
      ocrResult.text,
      { source: material.name, subject: material.subject, grade: material.grade }
    );
    results.push({ material: material.name, status: 'ingested', chunks: ragResult.chunks });
  }
  return results;
}
```

#### 2. 知识点图谱生成
```javascript
async function generateKnowledgeMap(subject, grade) {
  const result = await fetch('http://localhost:8905/analyze', {
    method: 'POST',
    body: JSON.stringify({
      type: 'knowledge_map',
      subject: subject,
      grade: grade,
      query: `http://localhost:8904/query?collection=teaching_kb&filter=subject:${subject}`
    })
  });
  const data = await result.json();
  
  // 在 p5.js 中可视化知识图谱
  drawKnowledgeGraph(data.nodes, data.edges);
}
```

#### 3. 智能教学检索
```javascript
async function smartSearch(query, filters = {}) {
  const result = await fetch('http://localhost:8904/query', {
    method: 'POST',
    body: JSON.stringify({
      query: query,
      top_k: 5,
      collection: 'teaching_kb',
      filters: filters,
      rerank: true
    })
  });
  return result.json();
}
```

### 产出规格
| 产出物 | 格式 | 质量标准 |
|--------|------|----------|
| 知识库 | ChromaDB 集合 | 分块合理，元数据完整 |
| 知识图谱 | p5.js 交互可视化 | 节点关系清晰，可交互探索 |
| 检索结果 | JSON + 高亮 | Top-5 相关，引用来源 |
| 知识报告 | HTML | 含覆盖率统计和薄弱点分析 |

### 评分映射
- **场景价值(30%)**: 教学资源从散乱到体系化，检索效率提升 5x
- **商用生产力(30%)**: 可部署为校本资源管理平台
- **工具使用(20%)**: OCR + RAG + Analysis 三工具联动
- **创新性(10%)**: 知识图谱可视化 + 智能检索融合

---

## 场景三：创意内容

### 场景描述
教学内容创意化：互动故事、配音课件、多媒体教材、创意作业设计。

### 工具链配置
```
ASR (port:8902) → 语音采集与评测
TTS (port:8903) → 多角色配音
OCR (port:8901) → 手绘素材识别
Gateway (port:8900) → 创作流水线
```

### 教学应用流程

#### 1. 互动英语故事（ASR + TTS）
```javascript
async function createInteractiveStory(storyData) {
  const toolbox = new AIToolbox('http://localhost:8900');
  
  // 为每个角色生成配音
  const voices = { narrator: 'xiaoyun', hero: 'xiaochen', villain: 'xiaomo' };
  for (const line of storyData.dialogues) {
    const audio = await toolbox.speakText(line.text, voices[line.character]);
    line.audioUrl = audio.audio_url;
  }
  
  // 生成 p5.js 互动场景
  return {
    story: storyData,
    interaction: {
      type: 'choice',
      points: storyData.decision_points,
      pronunciationPractice: true  // ASR 发音评测
    }
  };
}
```

#### 2. 手绘素材数字化（OCR → 课件）
```javascript
async function digitizeHandDrawnMaterial(sketchImage) {
  const toolbox = new AIToolbox('http://localhost:8900');
  
  // OCR 识别手绘内容
  const result = await toolbox.callTool('ocr', {
    image: sketchImage,
    mode: 'sketch',
    enhance: true
  });
  
  // 将识别结果融入 p5.js 课件
  return {
    extractedElements: result.elements,
    coursewareIntegration: true
  };
}
```

#### 3. 多媒体配音课件
```javascript
async function createDubbedCourseware(script, slides) {
  const toolbox = new AIToolbox('http://localhost:8900');
  
  // 为每页幻灯片生成配音
  const audioTracks = [];
  for (const slide of slides) {
    const audio = await toolbox.speakText(
      script[slide.id],
      'xiaoyun'
    );
    audioTracks.push({ slideId: slide.id, ...audio });
  }
  
  return { slides, audioTracks, syncMode: 'auto' };
}
```

### 产出规格
| 产出物 | 格式 | 质量标准 |
|--------|------|----------|
| 互动故事 | 单文件 HTML | 多角色配音，分支剧情，发音评测 |
| 数字化素材 | PNG + 元数据 | 手绘识别准确，矢量化可选 |
| 配音课件 | 单文件 HTML | 音画同步，自动播放控制 |
| 创意作业 | HTML 模板 | 支持多媒体提交，AI 辅助评价 |

### 评分映射
- **场景价值(30%)**: 让教学内容从静态到动态，学生参与度提升 3x
- **创新性(10%)**: ASR 发音评测 + 多角色 TTS + 手绘识别的创意融合
- **文章质量(10%)**: 互动体验流畅，音画同步精准
- **工具使用(20%)**: ASR + TTS + OCR 三工具协同

---

## 场景四：数据分析

### 场景描述
教学数据的智能分析：成绩分析、学情诊断、教学评估、趋势预测。

### 工具链配置
```
Analysis (port:8905) → 统计分析引擎
RAG (port:8904) → 教学常模知识库
OCR (port:8901) → 纸质试卷识别
Gateway (port:8900) → 分析流水线
```

### 教学应用流程

#### 1. 成绩智能分析
```javascript
async function analyzeExamResults(examData) {
  const result = await fetch('http://localhost:8905/analyze', {
    method: 'POST',
    body: JSON.stringify({
      type: 'exam_analysis',
      data: examData,
      analyses: ['statistics', 'distribution', 'knowledge_map', 'warnings']
    })
  });
  const data = await result.json();
  
  // p5.js 可视化面板
  const panel = new DataAnalysisPanel('analysis-container', {
    charts: [
      { type: 'bar', data: data.score_distribution, title: '成绩分布' },
      { type: 'radar', data: data.knowledge_mastery, title: '知识掌握度' },
      { type: 'line', data: data.trend, title: '趋势分析' }
    ],
    warnings: data.warnings,
    suggestions: data.suggestions
  });
  panel.render();
}
```

#### 2. 学情诊断报告
```javascript
async function generateDiagnosisReport(classId, semester) {
  const pipeline = new TeachingPipeline('http://localhost:8900');
  
  // 获取分析数据
  const analysis = await pipeline.runAnalysis('学情诊断', {
    class_id: classId,
    semester: semester,
    include: ['成绩统计', '知识图谱', '预警分析', '教学建议']
  });
  
  // 查询教学常模对比
  const norm = await pipeline.queryKnowledge(
    `${semester} 教学常模标准`,
    'teaching_norms'
  );
  
  return { analysis, normComparison: norm };
}
```

#### 3. 数据驱动教学调整
```javascript
async function suggestTeachingAdjustment(analysisResult) {
  const gateway = 'http://localhost:8900';
  
  // 基于分析结果生成教学建议
  const suggestions = analysisResult.weak_points.map(point => ({
    knowledge: point.name,
    mastery: point.score,
    action: point.score < 60 ? '重点补习' : point.score < 80 ? '巩固练习' : '拓展提升',
    resources: [] // 从 RAG 知识库匹配
  }));
  
  // 为每个建议匹配教学资源
  for (const s of suggestions) {
    const resources = await fetch(`${gateway}/api/rag/query`, {
      method: 'POST',
      body: JSON.stringify({
        query: `${s.knowledge} ${s.action} 教学资源`,
        top_k: 3,
        collection: 'teaching_resources'
      })
    });
    s.resources = (await resources.json()).results;
  }
  
  return suggestions;
}
```

### 产出规格
| 产出物 | 格式 | 质量标准 |
|--------|------|----------|
| 成绩分析报告 | HTML 仪表盘 | 含分布图/趋势图/预警，可交互 |
| 学情诊断 | HTML + 图表 | 知识图谱可视化，个性化建议 |
| 教学调整方案 | Markdown | 基于数据，引用常模对比 |
| 数据看板 | p5.js 嵌入 | 实时更新，响应式布局 |

### 评分映射
- **场景价值(30%)**: 从经验教学到数据驱动教学，精准定位学情
- **商用生产力(30%)**: 可部署为校级教学质量监控平台
- **工具使用(20%)**: Analysis + RAG + OCR 三工具联动
- **创新性(10%)**: AI 驱动的学情预警和教学建议

---

## 场景五：开发辅助

### 场景描述
辅助教师进行教学工具开发：课件模板开发、教学小程序、评估工具、自动化脚本。

### 工具链配置
```
全部工具 (port:8900-8905) → 完整工具链
Gateway (port:8900) → 开发辅助编排
```

### 教学应用流程

#### 1. 课件模板工厂
```javascript
async function generateCoursewareTemplate(subject, grade, topic) {
  const toolbox = new AIToolbox('http://localhost:8900');
  
  // 1. RAG 查询课标要求
  const standards = await toolbox.queryKnowledge(
    `${subject} ${grade} ${topic} 课程标准`,
    'curriculum_standards'
  );
  
  // 2. OCR 扫描现有教材相关页面
  // (教师拍照上传)
  
  // 3. 生成课件骨架
  const template = {
    subject, grade, topic,
    standards: standards.results,
    sections: [
      { type: 'intro', tools: ['tts'] },       // 导入：配音视频
      { type: 'lecture', tools: ['ocr'] },      // 讲授：数字化素材
      { type: 'practice', tools: ['asr'] },     // 练习：语音互动
      { type: 'assess', tools: ['analysis'] },  // 测评：数据分析
      { type: 'summary', tools: ['rag'] }       // 总结：知识检索
    ]
  };
  
  return template;
}
```

#### 2. 教学小程序生成
```javascript
async function generateTeachingApp(appSpec) {
  // 全工具链协作生成教学小程序
  const pipeline = new TeachingPipeline('http://localhost:8900');
  
  const app = {
    type: 'single-file-html',
    features: appSpec.features,
    aiTools: appSpec.required_tools.map(tool => ({
      name: tool,
      endpoint: `http://localhost:${TOOL_PORTS[tool]}`,
      fallback: 'cloud'
    })),
    offline: true,  // Service Worker
    responsive: true
  };
  
  return app;
}
```

#### 3. 自动化评估工具
```javascript
async function createAssessmentTool(assessmentSpec) {
  const gateway = 'http://localhost:8900';
  
  const tool = {
    name: assessmentSpec.name,
    type: 'assessment',
    components: [
      {
        type: 'question_bank',
        source: 'rag',
        collection: 'question_bank',
        filter: { subject: assessmentSpec.subject, difficulty: 'adaptive' }
      },
      {
        type: 'answer_capture',
        methods: ['text_input', 'voice_input', 'image_upload'],
        tools: { voice: 'asr', image: 'ocr' }
      },
      {
        type: 'scoring',
        methods: ['auto_match', 'ai_judge', 'rubric'],
        analysis: 'analysis'
      },
      {
        type: 'report',
        format: 'html_dashboard',
        include: ['score', 'analysis', 'suggestions', 'trend']
      }
    ]
  };
  
  return tool;
}
```

### 产出规格
| 产出物 | 格式 | 质量标准 |
|--------|------|----------|
| 课件模板 | 单文件 HTML | 含 AI 工具调用，可复用 |
| 教学小程序 | 单文件 HTML | 完整功能，离线可用 |
| 评估工具 | HTML + JSON | 自适应出题，自动评分 |
| 开发文档 | Markdown | API 说明，部署指南 |

### 评分映射
- **场景价值(30%)**: 降低教师开发门槛，从"不会做"到"AI 辅助做"
- **商用生产力(30%)**: 模板可复用，形成教学资源库
- **工具使用(20%)**: 全部 5 种工具协同，展示完整工具链
- **创新性(10%)**: AI 驱动的全栈教学工具开发
- **文章质量(10%)**: 代码质量高，文档完善

---

## 跨场景融合矩阵

展示五个场景之间的工具共享和流程衔接关系：

| 场景组合 | 融合方式 | 典型用例 |
|----------|----------|----------|
| 办公提效 + 知识管理 | OCR → 知识库入库 | 试卷扫描→自动归档→知识检索 |
| 知识管理 + 创意内容 | RAG → TTS 配音 | 检索教学素材→生成配音课件 |
| 创意内容 + 数据分析 | ASR → 分析面板 | 课堂录音→互动分析→教学改进 |
| 数据分析 + 开发辅助 | Analysis → 模板推荐 | 学情分析→自动推荐课件模板 |
| 全场景融合 | Pipeline 编排 | 教材数字化→知识库→配音课件→效果分析→迭代优化 |

## 评分自测清单

完成任一场景后，对照以下清单自评：

- [ ] 是否解决了真实教学痛点？（场景价值）
- [ ] 产出物是否可商用交付？（商用生产力）
- [ ] 是否使用了 ≥3 种本地 AI 工具？（工具使用）
- [ ] 产出物是否达到商用质量标准？（文章质量）
- [ ] 是否有创新性的工具组合或应用方式？（创新性）
- [ ] 是否附带 README + 演示 + 部署说明？（传播附加分）

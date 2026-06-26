# -*- coding: utf-8 -*-
# ============================================================
#  录音豆 · HTML 报告生成模块 v2
#  专业企业级会议纪要排版
# ============================================================

import os
import json
from datetime import datetime
from pathlib import Path

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ meeting_title }} · 会议纪要</title>
<style>
/* ─── Reset ─── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --primary: #1a3a5c;
  --primary-light: #2c5282;
  --accent: #2b6cb0;
  --accent-light: #ebf4ff;
  --red: #c53030;
  --red-light: #fff5f5;
  --green: #276749;
  --green-light: #f0fff4;
  --orange: #c05621;
  --orange-light: #fffaf0;
  --gray-100: #f7f8fa;
  --gray-200: #edf0f5;
  --gray-300: #d6dce8;
  --gray-500: #8896ab;
  --gray-700: #4a5568;
  --gray-900: #1a202c;
  --border: #d6dce8;
  --text: #1a202c;
  --text-sub: #4a5568;
  --radius: 6px;
  --shadow-sm: 0 1px 4px rgba(0,0,0,0.06);
  --shadow: 0 2px 12px rgba(0,0,0,0.08);
}

html { font-size: 14px; }
body {
  font-family: "PingFang SC", "Microsoft YaHei", "Noto Sans SC", sans-serif;
  background: #f0f2f7;
  color: var(--text);
  line-height: 1.75;
}

/* ─── 页面布局 ─── */
.page-wrap {
  max-width: 900px;
  margin: 0 auto;
  background: white;
  min-height: 100vh;
  box-shadow: 0 0 30px rgba(0,0,0,0.12);
}

/* ─── 文件头 ─── */
.doc-header {
  background: var(--primary);
  color: white;
  padding: 36px 48px 28px;
  position: relative;
}
.doc-header .doc-type {
  font-size: 11px;
  letter-spacing: 3px;
  text-transform: uppercase;
  opacity: 0.65;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.doc-header .doc-type::before {
  content: "";
  display: inline-block;
  width: 20px;
  height: 2px;
  background: rgba(255,255,255,0.5);
}
.doc-header h1 {
  font-size: 26px;
  font-weight: 700;
  letter-spacing: 0.5px;
  margin-bottom: 20px;
  line-height: 1.35;
}
.doc-header .header-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0;
  border-top: 1px solid rgba(255,255,255,0.15);
  padding-top: 16px;
  margin-top: 4px;
}
.doc-header .meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 20px 4px 0;
  margin-right: 20px;
  font-size: 12.5px;
  opacity: 0.82;
  border-right: 1px solid rgba(255,255,255,0.18);
}
.doc-header .meta-item:last-child { border-right: none; margin-right: 0; }
.doc-header .meta-item .label { opacity: 0.65; }
.doc-header .badge {
  position: absolute;
  top: 28px; right: 48px;
  background: rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 4px;
  padding: 4px 12px;
  font-size: 11px;
  letter-spacing: 1px;
  opacity: 0.8;
}

/* ─── 导航目录 ─── */
.toc-bar {
  background: var(--gray-100);
  border-bottom: 1px solid var(--border);
  padding: 0 48px;
  display: flex;
  gap: 0;
  overflow-x: auto;
  white-space: nowrap;
}
.toc-bar a {
  display: inline-block;
  padding: 12px 16px;
  font-size: 12.5px;
  color: var(--text-sub);
  text-decoration: none;
  border-bottom: 2px solid transparent;
  transition: all 0.15s;
}
.toc-bar a:hover { color: var(--accent); border-bottom-color: var(--accent); }

/* ─── 主体 ─── */
.doc-body { padding: 0 48px 60px; }

/* ─── Section ─── */
.section {
  margin-top: 40px;
  scroll-margin-top: 80px;
}
.section-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
  padding-bottom: 10px;
  border-bottom: 2px solid var(--gray-200);
}
.section-header .section-num {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px; height: 24px;
  background: var(--primary);
  color: white;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 700;
  flex-shrink: 0;
}
.section-header h2 {
  font-size: 15px;
  font-weight: 700;
  color: var(--primary);
  letter-spacing: 0.3px;
}

/* ─── 会议摘要 ─── */
.summary-box {
  background: var(--accent-light);
  border-left: 4px solid var(--accent);
  border-radius: 0 var(--radius) var(--radius) 0;
  padding: 18px 20px;
  font-size: 14px;
  line-height: 1.9;
  color: var(--primary-light);
}

/* ─── 基本信息表 ─── */
.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1px;
  background: var(--border);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
}
.info-item {
  background: white;
  padding: 12px 18px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
}
.info-item .info-label {
  font-size: 12px;
  color: var(--gray-500);
  white-space: nowrap;
  padding-top: 2px;
  min-width: 56px;
}
.info-item .info-value {
  font-size: 13.5px;
  color: var(--text);
  font-weight: 500;
}

/* ─── 参会人员 ─── */
.participants-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.person-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: var(--gray-100);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 5px 14px;
  font-size: 13px;
  color: var(--text);
}
.person-chip::before {
  content: "";
  width: 22px; height: 22px;
  background: var(--primary);
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  color: white;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='white'%3E%3Cpath d='M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z'/%3E%3C/svg%3E");
  background-size: 14px;
  background-repeat: no-repeat;
  background-position: center;
  flex-shrink: 0;
}

/* ─── 核心结论 ─── */
.conclusions-list {
  list-style: none;
  counter-reset: conclusion;
}
.conclusions-list li {
  counter-increment: conclusion;
  display: flex;
  gap: 14px;
  padding: 12px 0;
  border-bottom: 1px solid var(--gray-200);
  font-size: 13.5px;
  line-height: 1.75;
  align-items: flex-start;
}
.conclusions-list li:last-child { border-bottom: none; }
.conclusions-list li::before {
  content: counter(conclusion);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 22px; height: 22px;
  background: var(--accent-light);
  color: var(--accent);
  border-radius: 50%;
  font-size: 11px;
  font-weight: 700;
  flex-shrink: 0;
  margin-top: 2px;
}

/* ─── 决策事项 ─── */
.decision-list { display: flex; flex-direction: column; gap: 10px; }
.decision-card {
  background: white;
  border: 1px solid var(--border);
  border-left: 4px solid var(--primary);
  border-radius: 0 var(--radius) var(--radius) 0;
  padding: 14px 18px;
}
.decision-card .d-label {
  font-size: 11px;
  color: var(--gray-500);
  letter-spacing: 1px;
  text-transform: uppercase;
  margin-bottom: 5px;
}
.decision-card .d-content {
  font-size: 13.5px;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 6px;
}
.decision-card .d-rationale {
  font-size: 12.5px;
  color: var(--text-sub);
  padding-top: 6px;
  border-top: 1px dashed var(--gray-300);
}
.decision-card .d-rationale::before {
  content: "依据：";
  color: var(--gray-500);
}

/* ─── 行动项目 ─── */
.action-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.action-table thead tr {
  background: var(--gray-100);
}
.action-table th {
  padding: 10px 14px;
  text-align: left;
  font-weight: 600;
  color: var(--gray-700);
  font-size: 12px;
  letter-spacing: 0.5px;
  border-bottom: 2px solid var(--border);
}
.action-table td {
  padding: 12px 14px;
  border-bottom: 1px solid var(--gray-200);
  color: var(--text);
  vertical-align: top;
}
.action-table tr:last-child td { border-bottom: none; }
.action-table tr:hover td { background: var(--gray-100); }
.action-table .task-cell { font-weight: 500; }
.tag-owner {
  display: inline-block;
  background: var(--primary);
  color: white;
  border-radius: 3px;
  padding: 2px 9px;
  font-size: 11.5px;
}
.tag-deadline {
  display: inline-block;
  background: var(--orange-light);
  color: var(--orange);
  border: 1px solid #fbd38d;
  border-radius: 3px;
  padding: 2px 9px;
  font-size: 11.5px;
}
.tag-priority {
  display: inline-block;
  border-radius: 3px;
  padding: 2px 9px;
  font-size: 11px;
  font-weight: 600;
}
.tag-priority.high { background: #fff5f5; color: var(--red); border: 1px solid #fed7d7; }
.tag-priority.mid  { background: var(--orange-light); color: var(--orange); border: 1px solid #fbd38d; }
.tag-priority.low  { background: var(--green-light); color: var(--green); border: 1px solid #9ae6b4; }

/* ─── 议题详情 ─── */
.agenda-list { display: flex; flex-direction: column; gap: 16px; }
.agenda-item {
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
}
.agenda-head {
  display: flex;
  align-items: center;
  gap: 12px;
  background: var(--gray-100);
  padding: 12px 18px;
  border-bottom: 1px solid var(--border);
}
.agenda-head .agenda-num {
  font-size: 11px;
  color: var(--gray-500);
  background: var(--gray-200);
  border-radius: 3px;
  padding: 1px 7px;
  font-weight: 700;
}
.agenda-head .agenda-title {
  font-size: 13.5px;
  font-weight: 600;
  color: var(--primary);
  flex: 1;
}
.agenda-body { padding: 14px 18px; }
.agenda-points {
  list-style: none;
  margin-bottom: 10px;
}
.agenda-points li {
  display: flex;
  gap: 10px;
  font-size: 13px;
  color: var(--text-sub);
  padding: 4px 0;
  align-items: flex-start;
}
.agenda-points li::before {
  content: "·";
  color: var(--accent);
  font-size: 18px;
  line-height: 1.2;
  flex-shrink: 0;
}
.agenda-outcome {
  display: flex;
  gap: 8px;
  align-items: flex-start;
  background: var(--green-light);
  border-left: 3px solid var(--green);
  border-radius: 0 4px 4px 0;
  padding: 8px 14px;
  font-size: 12.5px;
  color: var(--green);
  margin-top: 8px;
}
.agenda-outcome::before { content: "结论："; font-weight: 600; white-space: nowrap; }

/* ─── 风险/跟进 ─── */
.warn-list { display: flex; flex-direction: column; gap: 8px; }
.warn-item {
  display: flex;
  gap: 10px;
  align-items: flex-start;
  background: var(--orange-light);
  border-left: 3px solid var(--orange);
  border-radius: 0 4px 4px 0;
  padding: 10px 14px;
  font-size: 13px;
  color: #744210;
}
.warn-item::before { content: "△"; flex-shrink: 0; font-weight: 700; color: var(--orange); }

/* ─── 下一步 ─── */
.nextsteps-list { counter-reset: nstep; list-style: none; }
.nextsteps-list li {
  counter-increment: nstep;
  display: flex;
  gap: 12px;
  padding: 11px 0;
  border-bottom: 1px solid var(--gray-200);
  font-size: 13.5px;
  align-items: flex-start;
}
.nextsteps-list li:last-child { border-bottom: none; }
.nextsteps-list li::before {
  content: counter(nstep, decimal-leading-zero);
  font-size: 11px;
  font-weight: 700;
  color: var(--accent);
  background: var(--accent-light);
  padding: 2px 6px;
  border-radius: 3px;
  flex-shrink: 0;
  margin-top: 2px;
}

/* ─── 完整转写 ─── */
.transcript-section {
  margin-top: 48px;
  border-top: 2px dashed var(--gray-300);
  padding-top: 32px;
}
.transcript-toggle {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  user-select: none;
  padding: 10px 0;
  color: var(--text-sub);
  font-size: 13px;
}
.transcript-toggle .toggle-icon {
  width: 18px; height: 18px;
  border: 1.5px solid var(--gray-500);
  border-radius: 3px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  transition: transform 0.2s;
}
details[open] .transcript-toggle .toggle-icon { transform: rotate(90deg); }
.transcript-body {
  background: var(--gray-100);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px 24px;
  max-height: 480px;
  overflow-y: auto;
  margin-top: 12px;
}
.seg-row {
  display: flex;
  gap: 12px;
  padding: 5px 0;
  align-items: flex-start;
  border-bottom: 1px solid var(--gray-200);
}
.seg-row:last-child { border-bottom: none; }
.seg-ts {
  font-family: "SF Mono", "Consolas", monospace;
  font-size: 11px;
  color: var(--gray-500);
  background: white;
  border: 1px solid var(--border);
  border-radius: 3px;
  padding: 1px 6px;
  white-space: nowrap;
  flex-shrink: 0;
  margin-top: 2px;
}
.seg-content { font-size: 13px; color: var(--text-sub); line-height: 1.7; }

/* ─── 页脚 ─── */
.doc-footer {
  background: var(--gray-100);
  border-top: 1px solid var(--border);
  padding: 16px 48px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 11.5px;
  color: var(--gray-500);
}

/* ─── 打印 ─── */
@media print {
  body { background: white; }
  .page-wrap { box-shadow: none; }
  .toc-bar { display: none; }
  .transcript-section { display: none; }
  .section { page-break-inside: avoid; }
  .doc-header { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
}

@media (max-width: 700px) {
  .doc-header, .doc-body { padding-left: 20px; padding-right: 20px; }
  .toc-bar { padding: 0 20px; }
  .doc-footer { padding: 12px 20px; flex-direction: column; gap: 4px; text-align: center; }
  .info-grid { grid-template-columns: 1fr; }
  .header-meta { flex-direction: column; gap: 8px; }
  .meta-item { border-right: none; }
}
</style>
</head>
<body>
<div class="page-wrap">

<!-- ── 文档头 ─────────────────────────────────────── -->
<div class="doc-header">
  <div class="badge">会议纪要</div>
  <div class="doc-type">MEETING MINUTES · {{ meeting_type }}</div>
  <h1>{{ meeting_title }}</h1>
  <div class="header-meta">
    <div class="meta-item"><span class="label">日期</span> {{ meeting_date }}</div>
    <div class="meta-item"><span class="label">录音时长</span> {{ audio_duration }}</div>
    <div class="meta-item"><span class="label">转写字数</span> {{ word_count }} 字</div>
    {% if audio_filename %}<div class="meta-item"><span class="label">来源文件</span> {{ audio_filename }}</div>{% endif %}
  </div>
</div>

<!-- ── 导航目录 ───────────────────────────────────── -->
<div class="toc-bar">
  <a href="#sec-summary">会议概述</a>
  {% if participants %}<a href="#sec-participants">参会人员</a>{% endif %}
  {% if key_conclusions %}<a href="#sec-conclusions">核心结论</a>{% endif %}
  {% if decisions %}<a href="#sec-decisions">决策事项</a>{% endif %}
  {% if action_items %}<a href="#sec-actions">行动项目</a>{% endif %}
  {% if agenda_items %}<a href="#sec-agenda">议题详情</a>{% endif %}
  {% if next_steps %}<a href="#sec-nextsteps">后续计划</a>{% endif %}
  {% if risks_and_concerns %}<a href="#sec-risks">风险跟进</a>{% endif %}
</div>

<!-- ── 正文 ─────────────────────────────────────── -->
<div class="doc-body">

  <!-- 1. 会议概述 -->
  <div class="section" id="sec-summary">
    <div class="section-header">
      <span class="section-num">1</span>
      <h2>会议概述</h2>
    </div>
    <div class="summary-box">{{ meeting_summary }}</div>
  </div>

  <!-- 2. 参会人员 -->
  {% if participants %}
  <div class="section" id="sec-participants">
    <div class="section-header">
      <span class="section-num">2</span>
      <h2>参会人员</h2>
    </div>
    <div class="participants-list">
      {% for p in participants %}
      <div class="person-chip">{{ p }}</div>
      {% endfor %}
    </div>
  </div>
  {% endif %}

  <!-- 3. 核心结论 -->
  {% if key_conclusions %}
  <div class="section" id="sec-conclusions">
    <div class="section-header">
      <span class="section-num">{% if participants %}3{% else %}2{% endif %}</span>
      <h2>核心结论</h2>
    </div>
    <ol class="conclusions-list">
      {% for point in key_conclusions %}
      <li>{{ point }}</li>
      {% endfor %}
    </ol>
  </div>
  {% endif %}

  <!-- 4. 决策事项 -->
  {% if decisions %}
  <div class="section" id="sec-decisions">
    <div class="section-header">
      <span class="section-num">★</span>
      <h2>决策事项</h2>
    </div>
    <div class="decision-list">
      {% for d in decisions %}
      <div class="decision-card">
        <div class="d-label">已确认决策</div>
        <div class="d-content">{{ d.content if d is mapping else d }}</div>
        {% if d is mapping and d.rationale %}
        <div class="d-rationale">{{ d.rationale }}</div>
        {% endif %}
      </div>
      {% endfor %}
    </div>
  </div>
  {% endif %}

  <!-- 5. 行动项目 -->
  {% if action_items %}
  <div class="section" id="sec-actions">
    <div class="section-header">
      <span class="section-num">✓</span>
      <h2>行动项目</h2>
    </div>
    <table class="action-table">
      <thead>
        <tr>
          <th style="width:36px">#</th>
          <th>行动任务</th>
          <th style="width:90px">负责人</th>
          <th style="width:110px">截止时间</th>
          <th style="width:70px">优先级</th>
        </tr>
      </thead>
      <tbody>
        {% for item in action_items %}
        <tr>
          <td style="color:var(--gray-500); font-size:12px">{{ "%02d"|format(loop.index) }}</td>
          <td class="task-cell">
            {% if item is mapping %}{{ item.task }}{% else %}{{ item }}{% endif %}
          </td>
          <td>
            {% if item is mapping %}
            <span class="tag-owner">{{ item.owner }}</span>
            {% endif %}
          </td>
          <td>
            {% if item is mapping %}
            <span class="tag-deadline">{{ item.deadline }}</span>
            {% endif %}
          </td>
          <td>
            {% if item is mapping and item.priority %}
              {% if item.priority in ('高', 'high', 'High') %}
              <span class="tag-priority high">高</span>
              {% elif item.priority in ('低', 'low', 'Low') %}
              <span class="tag-priority low">低</span>
              {% else %}
              <span class="tag-priority mid">中</span>
              {% endif %}
            {% endif %}
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
  {% endif %}

  <!-- 6. 议题详情 -->
  {% if agenda_items %}
  <div class="section" id="sec-agenda">
    <div class="section-header">
      <span class="section-num">■</span>
      <h2>议题详情</h2>
    </div>
    <div class="agenda-list">
      {% for item in agenda_items %}
      <div class="agenda-item">
        <div class="agenda-head">
          <span class="agenda-num">议题 {{ loop.index }}</span>
          <span class="agenda-title">{{ item.title if item is mapping else item }}</span>
        </div>
        {% if item is mapping %}
        <div class="agenda-body">
          {% if item.key_points %}
          <ul class="agenda-points">
            {% for kp in item.key_points %}
            <li>{{ kp }}</li>
            {% endfor %}
          </ul>
          {% endif %}
          {% if item.outcome %}
          <div class="agenda-outcome">{{ item.outcome }}</div>
          {% endif %}
        </div>
        {% endif %}
      </div>
      {% endfor %}
    </div>
  </div>
  {% endif %}

  <!-- 7. 后续计划 -->
  {% if next_steps %}
  <div class="section" id="sec-nextsteps">
    <div class="section-header">
      <span class="section-num">→</span>
      <h2>后续计划</h2>
    </div>
    <ol class="nextsteps-list">
      {% for step in next_steps %}
      <li>{{ step }}</li>
      {% endfor %}
    </ol>
  </div>
  {% endif %}

  <!-- 8. 风险与跟进 -->
  {% if risks_and_concerns or follow_up_required %}
  <div class="section" id="sec-risks">
    <div class="section-header">
      <span class="section-num">!</span>
      <h2>风险与待跟进事项</h2>
    </div>
    <div class="warn-list">
      {% for risk in risks_and_concerns %}
      <div class="warn-item">{{ risk }}</div>
      {% endfor %}
      {% if follow_up_required %}
        {% for f in follow_up_required %}
        <div class="warn-item">{{ f }}</div>
        {% endfor %}
      {% endif %}
    </div>
  </div>
  {% endif %}

  <!-- 完整转写记录 -->
  <div class="transcript-section">
    <details>
      <summary class="transcript-toggle">
        <div class="toggle-icon">▶</div>
        完整文字转写记录（点击展开）
      </summary>
      <div class="transcript-body">
        {% if segments %}
          {% for seg in segments %}
          <div class="seg-row">
            <span class="seg-ts">{{ seg.start_fmt }}</span>
            <span class="seg-content">{{ seg.text }}</span>
          </div>
          {% endfor %}
        {% else %}
          <div style="font-size:13px; color:var(--text-sub); white-space:pre-wrap; line-height:1.9">{{ full_text }}</div>
        {% endif %}
      </div>
    </details>
  </div>

</div><!-- /.doc-body -->

<!-- ── 页脚 ────────────────────────────────────── -->
<div class="doc-footer">
  <span>由 🫘 录音豆 自动生成 · {{ generated_at }}</span>
  <span>本文件由 AI 辅助整理，请以实际会议结果为准</span>
</div>

</div><!-- /.page-wrap -->
</body>
</html>"""


def render_html(
    summary: dict,
    transcript: dict,
    audio_filename: str = "",
    output_path: str = None,
) -> str:
    try:
        from jinja2 import Template
    except ImportError:
        return _render_without_jinja(summary, transcript, audio_filename, output_path)

    duration_sec = transcript.get("duration_seconds", 0)
    if duration_sec > 0:
        h, m, s = int(duration_sec // 3600), int((duration_sec % 3600) // 60), int(duration_sec % 60)
        audio_duration = f"{h:02d}:{m:02d}:{s:02d}" if h > 0 else f"{m:02d}:{s:02d}"
    else:
        audio_duration = "未知"

    now = datetime.now()

    # 兼容新旧字段
    key_conclusions = summary.get("key_conclusions", summary.get("key_points", []))
    agenda_items = summary.get("agenda_items", summary.get("topics_discussed", []))
    risks = summary.get("risks_and_concerns", summary.get("unresolved_issues", []))
    follow_up = summary.get("follow_up_required", [])
    meeting_type = summary.get("meeting_type", "会议")

    context = {
        "meeting_title": summary.get("meeting_title", "会议纪要"),
        "meeting_type": meeting_type,
        "meeting_date": now.strftime("%Y年%m月%d日 %H:%M"),
        "audio_duration": audio_duration,
        "word_count": len(transcript.get("text", "")),
        "audio_filename": audio_filename,
        "meeting_summary": summary.get("meeting_summary", ""),
        "key_conclusions": key_conclusions,
        "decisions": summary.get("decisions", []),
        "action_items": summary.get("action_items", []),
        "participants": summary.get("participants", []),
        "agenda_items": agenda_items,
        "next_steps": summary.get("next_steps", []),
        "risks_and_concerns": risks,
        "follow_up_required": follow_up,
        "segments": transcript.get("segments", []),
        "full_text": transcript.get("text", ""),
        "generated_at": now.strftime("%Y-%m-%d %H:%M:%S"),
    }

    template = Template(HTML_TEMPLATE)
    html = template.render(**context)

    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        return output_path
    return html


def _render_without_jinja(summary, transcript, audio_filename, output_path):
    import re
    html = HTML_TEMPLATE
    replacements = {
        "{{ meeting_title }}": summary.get("meeting_title", "会议纪要"),
        "{{ meeting_type }}": summary.get("meeting_type", "会议"),
        "{{ meeting_date }}": datetime.now().strftime("%Y年%m月%d日 %H:%M"),
        "{{ audio_duration }}": "未知",
        "{{ word_count }}": str(len(transcript.get("text", ""))),
        "{{ audio_filename }}": audio_filename or "",
        "{{ meeting_summary }}": summary.get("meeting_summary", ""),
        "{{ full_text }}": transcript.get("text", "").replace("<", "&lt;").replace(">", "&gt;"),
        "{{ generated_at }}": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    for k, v in replacements.items():
        html = html.replace(k, str(v))
    html = re.sub(r'\{%-?\s*if.*?-?%\}.*?\{%-?\s*endif\s*-?%\}', '', html, flags=re.DOTALL)
    html = re.sub(r'\{%-?\s*for.*?-?%\}.*?\{%-?\s*endfor\s*-?%\}', '', html, flags=re.DOTALL)
    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        return output_path
    return html

#!/usr/bin/env node
/**
 * setup.mjs - 深层记忆系统初始化脚本
 *
 * 安装 skill 后运行一次即可：
 *   node skills/depth-memory/scripts/setup.mjs
 *
 * 功能：
 *   1. 在工作区根目录创建 DEEP-MEMORY.md（若不存在）
 *   2. 创建 deep-memory/ 目录（若不存在）
 *   3. 写入一条验收测试记录
 *   4. 更新 DEEP-MEMORY.md 索引
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const WORKSPACE = resolve(__dirname, '../../..');  // skills/depth-memory/scripts/.. -> workspace
const DEEP_MEM = resolve(WORKSPACE, 'DEEP-MEMORY.md');
const DEEP_MEM_DIR = resolve(WORKSPACE, 'deep-memory');
const TEST_FILE = resolve(DEEP_MEM_DIR, '2026-05-07 11_01_00.md');
const TEST_KEYWORD = '深层记忆系统验收测试';

const TEST_RECORD = `# ${TEST_KEYWORD}

> 来源：skill 初始化自动生成
> 存入时间：2026-05-07 11:01

## 概述

这是深层记忆系统安装时自动生成的验收测试记录。若能搜到此条记录，说明深层记忆系统工作正常。

## 验证方法

在 DEEP-MEMORY.md 索引中搜索关键字：**${TEST_KEYWORD}** 或 **验收测试**

成功命中即代表系统就绪。
`;

const TEMPLATE_DEEP_MEMORY = `# 深层记忆索引 (Deep Memory Index)

这是系统的长期知识库。如果你在 MEMORY.md 中找不到答案，请查阅下表，匹配 \`Keywords\`，并使用读取文件工具查看对应的 \`File Path\`。

| Keywords (关键字) | Description (概要说明) | File Path (文件路径) |
| :--- | :--- | :--- |
`;

const TEMPLATE_INDEX_ROW = `| ${TEST_KEYWORD}, 验收测试, 深层记忆系统验证 | 深层记忆系统安装验收测试记录，验证系统是否正常工作 | \`deep-memory/2026-05-07 11_01_00.md\` |`;

function log(msg) { console.log(`[depth-memory setup] ${msg}`); }

function init() {
  log(`工作区: ${WORKSPACE}`);

  // 1. 创建 deep-memory/ 目录
  if (!existsSync(DEEP_MEM_DIR)) {
    mkdirSync(DEEP_MEM_DIR, { recursive: true });
    log(`创建目录: deep-memory/`);
  } else {
    log(`目录已存在: deep-memory/`);
  }

  // 2. 写入测试记忆文件
  if (!existsSync(TEST_FILE)) {
    writeFileSync(TEST_FILE, TEST_RECORD, 'utf-8');
    log(`写入测试记录: ${TEST_FILE}`);
  } else {
    log(`测试记录已存在，跳过`);
  }

  // 3. 创建 DEEP-MEMORY.md（若不存在）
  if (!existsSync(DEEP_MEM)) {
    writeFileSync(DEEP_MEM, TEMPLATE_DEEP_MEMORY.trim() + '\n', 'utf-8');
    log(`创建索引: DEEP-MEMORY.md`);
  } else {
    log(`索引已存在: DEEP-MEMORY.md`);
  }

  // 4. 将测试记录写入索引（若不在索引中）
  const content = readFileSync(DEEP_MEM, 'utf-8');
  if (!content.includes(TEST_KEYWORD)) {
    const updated = content.trimEnd() + '\n' + TEMPLATE_INDEX_ROW + '\n';
    writeFileSync(DEEP_MEM, updated, 'utf-8');
    log(`更新索引：加入测试记录`);
  } else {
    log(`索引已有测试记录，跳过`);
  }

  log(`初始化完成！`);
  log(`\n验证：搜索关键字"${TEST_KEYWORD}"应能命中此条记录。`);
}

init();
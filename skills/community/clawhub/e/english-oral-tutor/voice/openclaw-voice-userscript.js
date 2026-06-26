// ==UserScript==
// @name         OpenClaw English Oral Voice
// @namespace    openclaw-oral-voice
// @version      1.14
// @description  浏览器语音输入(STT) + 语音输出(TTS)，用于 OpenClaw Control UI 英语口语练习
// @author       oral-app
// @match        http://127.0.0.1:18789/*
// @match        http://localhost:18789/*
// @match        http://192.168.*:18789/*
// @grant        none
// @run-at       document-idle
// ==/UserScript==

(function () {
  'use strict';

  const DEBUG = true;
  function log(...args) { if (DEBUG) console.log('[oral-voice]', ...args); }

  // ===================================================================
  //  全局状态
  // ===================================================================
  let recognition = null;       // SpeechRecognition 实例
  let isRecording = false;      // 是否正在录音
  let ttsEnabled = true;        // 语音输出开关
  let volume = 0.8;             // 音量 0-1
  let rate = 1.10;              // 语速 0.5-2.0
  let currentUtterance = null;  // 当前正在播放的 utterance
  let speechQueue = [];         // 待朗读的句子队列
  let isSpeaking = false;       // 是否正在朗读
  let ttsTimeout = null;        // TTS 超时定时器（防止浏览器挂起后队列永久卡死）
  let debounceTimer = null;     // MutationObserver 的防抖定时器

  // ===================================================================
  //  DOM 等待工具
  //  轮询等待指定选择器的元素出现在页面上（最长等 timeoutMs 毫秒）
  // ===================================================================
  function waitFor(selector, timeoutMs = 20000) {
    return new Promise((resolve, reject) => {
      const el = document.querySelector(selector);
      if (el && el.offsetParent !== null) return resolve(el);
      const obs = new MutationObserver(() => {
        const el = document.querySelector(selector);
        if (el && el.offsetParent !== null) { obs.disconnect(); resolve(el); }
      });
      obs.observe(document.body, { childList: true, subtree: true });
      setTimeout(() => { obs.disconnect(); reject(new Error('timeout: ' + selector)); }, timeoutMs);
    });
  }

  // ===================================================================
  //  语音控制面板 UI
  //  注入到页面左下角（侧边栏底部），可拖放移动位置
  //  包含：麦克风按钮、喇叭开关、音量滑轨、语速滑轨
  // ===================================================================
  function injectToolbar() {
    const html = `
      <div id="oral-voice-toolbar">
        <style>
          /* 面板容器 —— 固定在左下角，侧边栏范围内 */
          #oral-voice-toolbar {
            position: fixed;
            bottom: 12px;
            left: 10px;
            z-index: 999999;
            width: 238px;
            background: rgba(15, 23, 42, 0.92);
            border: 1px solid rgba(233, 69, 96, 0.25);
            border-radius: 12px;
            padding: 8px 10px;
            backdrop-filter: blur(12px);
            box-shadow: 0 4px 16px rgba(0,0,0,0.4);
            font-family: system-ui, sans-serif;
            user-select: none;
            display: flex;
            flex-direction: column;
            gap: 6px;
          }
          #oral-voice-toolbar .v-row {
            display: flex;
            align-items: center;
            gap: 8px;
          }
          #oral-voice-toolbar .v-row--controls {
            justify-content: space-between;
          }
          /* 圆形按钮通用样式 */
          #oral-voice-toolbar button {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            border: none;
            cursor: pointer;
            font-size: 1rem;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s;
            color: #fff;
            flex-shrink: 0;
          }
          /* 麦克风按钮 */
          #oral-voice-toolbar .v-mic {
            background: #e94560;
          }
          #oral-voice-toolbar .v-mic:hover { background: #d13450; transform: scale(1.05); }
          /* 录音中状态 —— 绿色脉动动画 */
          #oral-voice-toolbar .v-mic.recording {
            background: #22c55e;
            animation: ov-pulse 1.2s infinite;
            box-shadow: 0 0 12px rgba(34,197,94,0.5);
          }
          /* 喇叭按钮 */
          #oral-voice-toolbar .v-speaker {
            background: #334155;
          }
          #oral-voice-toolbar .v-speaker:hover { background: #475569; }
          /* 静音状态 */
          #oral-voice-toolbar .v-speaker.muted {
            background: #1e293b;
            opacity: 0.5;
          }
          /* 滑轨组 */
          #oral-voice-toolbar .v-slider-group {
            display: flex;
            align-items: center;
            gap: 4px;
            flex: 1;
            min-width: 0;
          }
          #oral-voice-toolbar .v-slider-group span {
            color: #94a3b8;
            font-size: 0.65rem;
            flex-shrink: 0;
            width: 18px;
            text-align: center;
          }
          #oral-voice-toolbar input[type="range"] {
            flex: 1;
            min-width: 0;
            accent-color: #e94560;
            height: 4px;
            cursor: pointer;
          }
          /* 拖动手柄 —— "VOICE" 标签 */
          #oral-voice-toolbar .v-label {
            color: #64748b;
            font-size: 0.55rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            cursor: grab;
            user-select: none;
          }
          #oral-voice-toolbar.dragging .v-label {
            cursor: grabbing;
          }
          /* 语音识别实时文本显示 */
          #oral-stt-interim {
            position: fixed;
            bottom: 120px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(233,69,96,0.9);
            color: #fff;
            padding: 10px 24px;
            border-radius: 24px;
            font-size: 1rem;
            font-family: system-ui, sans-serif;
            z-index: 999999;
            display: none;
            max-width: 70vw;
            text-align: center;
            pointer-events: none;
            box-shadow: 0 4px 16px rgba(0,0,0,0.3);
          }
          @keyframes ov-pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.18); }
          }
        </style>
        <!-- 第一行：标签 + 喇叭开关 + 麦克风 -->
        <div class="v-row v-row--controls">
          <span class="v-label">Voice</span>
          <button class="v-speaker" id="v-speaker-btn" title="Toggle voice output">🔊</button>
          <button class="v-mic" id="v-mic-btn" title="Click to start/stop recording">🎤</button>
        </div>
        <!-- 第二行：音量滑轨 -->
        <div class="v-slider-group">
          <span>🔊</span>
          <input type="range" id="v-volume" min="0" max="100" value="80" title="Volume">
        </div>
        <!-- 第三行：语速滑轨（🐢慢 ↔ 🐇快） -->
        <div class="v-slider-group">
          <span>🐢</span>
          <input type="range" id="v-rate" min="50" max="200" value="110" title="Speed">
          <span>🐇</span>
        </div>
      </div>
      <div id="oral-stt-interim"></div>
    `;
    document.body.insertAdjacentHTML('beforeend', html);

    // ---- 获取 DOM 引用 ----
    const micBtn = document.getElementById('v-mic-btn');
    const speakerBtn = document.getElementById('v-speaker-btn');
    const volumeSlider = document.getElementById('v-volume');
    const rateSlider = document.getElementById('v-rate');

    // ---- 音量滑轨：拖动时中断当前朗读并更新 ----
    volumeSlider.addEventListener('input', () => {
      volume = parseInt(volumeSlider.value) / 100;
      window.speechSynthesis.cancel();
      speechQueue = [];
      isSpeaking = false;
    });

    // ---- 语速滑轨：拖动时中断当前朗读并更新 ----
    rateSlider.addEventListener('input', () => {
      rate = parseInt(rateSlider.value) / 100;
      window.speechSynthesis.cancel();
      speechQueue = [];
      isSpeaking = false;
    });

    // ---- 麦克风按钮：点击切换录音状态 ----
    micBtn.addEventListener('click', () => {
      if (!recognition) initSTT();
      if (isRecording) stopRecording(); else startRecording();
    });

    // ---- 喇叭按钮：切换语音输出开关 ----
    speakerBtn.addEventListener('click', () => {
      ttsEnabled = !ttsEnabled;
      speakerBtn.classList.toggle('muted', !ttsEnabled);
      speakerBtn.textContent = ttsEnabled ? '🔊' : '🔇';
      if (!ttsEnabled) { window.speechSynthesis.cancel(); speechQueue = []; isSpeaking = false; }
    });

    // ---- 面板拖放功能 ----
    // 按住 "VOICE" 标签即可拖动整个面板，限制在视口内
    const toolbar = document.getElementById('oral-voice-toolbar');
    const dragHandle = toolbar.querySelector('.v-label');
    let dragging = false, dragStartX = 0, dragStartY = 0, panelStartX = 0, panelStartY = 0;

    dragHandle.addEventListener('mousedown', (e) => {
      if (e.button !== 0) return;  // 只响应左键
      dragging = true;
      toolbar.classList.add('dragging');
      const rect = toolbar.getBoundingClientRect();
      // 将 CSS 的 bottom/left 定位转换为 top/left 以便拖放计算
      toolbar.style.top = rect.top + 'px';
      toolbar.style.left = rect.left + 'px';
      toolbar.style.bottom = 'auto';
      toolbar.style.right = 'auto';
      dragStartX = e.clientX;
      dragStartY = e.clientY;
      panelStartX = rect.left;
      panelStartY = rect.top;
      e.preventDefault();
    });

    document.addEventListener('mousemove', (e) => {
      if (!dragging) return;
      const dx = e.clientX - dragStartX;
      const dy = e.clientY - dragStartY;
      let newX = panelStartX + dx;
      let newY = panelStartY + dy;
      // 限制在视口内，防止拖出屏幕
      const w = toolbar.offsetWidth;
      const h = toolbar.offsetHeight;
      newX = Math.max(0, Math.min(newX, window.innerWidth - w));
      newY = Math.max(0, Math.min(newY, window.innerHeight - h));
      toolbar.style.left = newX + 'px';
      toolbar.style.top = newY + 'px';
    });

    document.addEventListener('mouseup', () => {
      if (!dragging) return;
      dragging = false;
      toolbar.classList.remove('dragging');
    });

    return { micBtn, speakerBtn, volumeSlider, rateSlider };
  }

  // ===================================================================
  //  STT: 语音识别（Speech-to-Text）
  //  使用浏览器 Web Speech API 的 SpeechRecognition
  //  支持连续识别 + 实时 interim 显示
  // ===================================================================
  function initSTT() {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) {
      alert('Speech recognition not supported. Please use Chrome or Edge.');
      return;
    }
    recognition = new SR();
    recognition.lang = 'en-US';           // 英语识别
    recognition.continuous = true;        // 持续识别（不停）
    recognition.interimResults = true;    // 返回 interim 结果（边说边显示）
    recognition.maxAlternatives = 1;      // 只取最可能的识别结果

    // 识别结果回调
    recognition.onresult = (event) => {
      let finalText = '', interimText = '';
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const t = event.results[i][0].transcript;
        if (event.results[i].isFinal) finalText += t + ' ';
        else interimText += t;
      }
      // 屏幕中央显示实时识别文字
      const interimEl = document.getElementById('oral-stt-interim');
      if (interimEl) {
        interimEl.style.display = interimText ? 'block' : 'none';
        interimEl.textContent = interimText;
      }
      // 最终结果 → 填入聊天输入框，不自动发送（用户手动点发送）
      if (finalText.trim()) {
        fillChatInput(finalText.trim());
        stopRecording();
      }
    };

    // 错误处理
    recognition.onerror = (e) => {
      log('STT error:', e.error);
      if (e.error === 'not-allowed') {
        alert('Microphone access denied. Please allow it in browser settings.');
        stopRecording();
      }
    };

    // 录音结束后自动重启（实现连续录音；用户手动点停止才真正停）
    recognition.onend = () => {
      if (isRecording) {
        try { recognition.start(); } catch (_) { stopRecording(); }
      }
    };
  }

  // 开始录音
  function startRecording() {
    if (!recognition) initSTT();
    if (!recognition) return;
    isRecording = true;
    const micBtn = document.getElementById('v-mic-btn');
    if (micBtn) micBtn.classList.add('recording');
    try { recognition.start(); } catch (_) {}
    log('Recording...');
  }

  // 停止录音
  function stopRecording() {
    isRecording = false;
    const micBtn = document.getElementById('v-mic-btn');
    if (micBtn) micBtn.classList.remove('recording');
    const interimEl = document.getElementById('oral-stt-interim');
    if (interimEl) interimEl.style.display = 'none';
    try { recognition.stop(); } catch (_) {}
    log('Stopped');
  }

  // ===================================================================
  //  向 Control UI 发送消息
  //  通过 DOM 操作注入文本到输入框，触发 Vue 响应，然后点击发送按钮
  // ===================================================================

  // 查找 Control UI 的聊天输入框
  function findChatInput() {
    const selectors = [
      '.chat-compose__field textarea',
      '.agent-chat__input textarea',
      '.chat-compose textarea',
      'textarea',
    ];
    for (const sel of selectors) {
      const el = document.querySelector(sel);
      if (el && el.offsetParent !== null) return el;
    }
    return null;
  }

  // 查找发送按钮
  function findSendButton() {
    const selectors = [
      '.chat-send-btn',
      '.chat-compose__actions button:last-child',
      '.agent-chat__input-btn:last-of-type',
    ];
    for (const sel of selectors) {
      const el = document.querySelector(sel);
      if (el && el.offsetParent !== null) return el;
    }
    // 兜底：在输入区域找最短文字的按钮（通常是发送图标按钮）
    const compose = document.querySelector('.chat-compose, .agent-chat__input');
    if (compose) {
      const btns = compose.querySelectorAll('button');
      for (const b of btns) {
        if (b.offsetParent !== null && b.textContent.trim().length <= 2) return b;
      }
    }
    return null;
  }

  // 将文字追加到聊天输入框（不发送，由用户手动点击发送按钮）
  function fillChatInput(text) {
    const input = findChatInput();
    if (!input) { log('No input found'); return; }

    // 获取当前内容，追加新文本（用空格分隔）
    const currentValue = input.value || '';
    const newValue = currentValue.trim()
      ? currentValue + ' ' + text.trim()
      : text.trim();

    // 使用原生 value setter（触发 Vue v-model 响应）
    const proto = input.tagName === 'TEXTAREA'
      ? HTMLTextAreaElement : HTMLInputElement;
    const desc = Object.getOwnPropertyDescriptor(proto.prototype, 'value');
    if (desc && desc.set) {
      desc.set.call(input, newValue);
    } else {
      input.value = newValue;
    }
    // 派发事件让 Vue 感知变化
    input.dispatchEvent(new Event('input', { bubbles: true }));
    input.dispatchEvent(new Event('change', { bubbles: true }));
    // 聚焦输入框，方便用户编辑确认后手动发送
    input.focus();
    log('Appended:', text.slice(0, 60), '| Total:', newValue.length);
  }

  // 填入文字并点击发送（用于需要自动发送的场景）
  function sendAsChatMessage(text) {
    fillChatInput(text);
    const input = findChatInput();
    if (!input) { log('No input found'); return; }

    // 延迟点击发送（等 Vue 完成响应式更新）
    setTimeout(() => {
      const sendBtn = findSendButton();
      if (sendBtn) {
        sendBtn.click();
        log('Sent:', text.slice(0, 60));
      } else {
        // 找不到按钮时按回车兜底
        input.dispatchEvent(new KeyboardEvent('keydown', {
          key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true, cancelable: true
        }));
        log('Sent via Enter:', text.slice(0, 60));
      }
    }, 150);
  }

  // ===================================================================
  //  TTS: 语音合成（Text-to-Speech）
  //  使用浏览器 Web Speech API 的 SpeechSynthesis
  //  句子队列 → 逐个朗读，自动衔接
  // ===================================================================

  // 处理朗读队列
  function processSpeechQueue() {
    if (isSpeaking || speechQueue.length === 0) return;
    if (!ttsEnabled) { speechQueue = []; return; }
    isSpeaking = true;
    const text = speechQueue.shift();
    const synth = window.speechSynthesis;
    const u = new SpeechSynthesisUtterance(text);
    u.lang = 'en-US';
    u.rate = rate;       // 用户可调语速
    u.volume = volume;   // 用户可调音量
    u.pitch = 1.0;

    // 优先选 Google Female → Natural → 任意 US Female → 任意 US
    const voices = synth.getVoices();
    const pref = voices.find(v => v.lang.startsWith('en') && v.name.includes('Google') && v.name.includes('Female'))
      || voices.find(v => v.lang.startsWith('en') && v.name.includes('Natural'))
      || voices.find(v => v.lang.startsWith('en-US') && v.name.includes('Female'))
      || voices.find(v => v.lang.startsWith('en-US'));
    if (pref) u.voice = pref;

    currentUtterance = u;
    // 清除旧超时，设置新的 30 秒超时保护
    if (ttsTimeout) clearTimeout(ttsTimeout);
    ttsTimeout = setTimeout(() => {
      if (currentUtterance === u) {
        // 浏览器 TTS 挂起：speak() 生效但 onend 永不触发
        log('TTS timeout — resetting stuck utterance');
        currentUtterance = null;
        isSpeaking = false;
        window.speechSynthesis.cancel();
        // 用 pause+resume trick 尝试恢复 Chrome speechSynthesis
        window.speechSynthesis.pause();
        window.speechSynthesis.resume();
        processSpeechQueue();
      }
    }, 30000);
    const next = () => { currentUtterance = null; isSpeaking = false; if (ttsTimeout) clearTimeout(ttsTimeout); setTimeout(processSpeechQueue, 40); };
    u.onend = next;
    u.onerror = next;
    synth.speak(u);
  }

  // 将文本拆成句子加入队列
  function enqueueTTS(text) {
    if (!ttsEnabled || !text || !text.trim()) return;
    // 唤醒被浏览器挂起的 speechSynthesis 实例
    window.speechSynthesis.cancel();
    // 清空旧队列（cancel 已停掉当前播放，旧内容无需保留）
    speechQueue = [];
    // 按标点拆句，让朗读节奏自然
    const sentences = text.match(/[^.!?\n]+[.!?\n]?/g) || [text];
    for (const s of sentences) {
      const clean = s.trim();
      if (clean) speechQueue.push(clean);
    }
    if (!isSpeaking) processSpeechQueue();
  }

  // ===================================================================
  //  AI 消息监测
  //
  //  Control UI 的 DOM 结构：
  //    .chat-group.assistant > .chat-group-messages > .chat-msg > .chat-bubble
  //    .chat-group（无 "assistant" 类）= 用户/系统消息
  //
  //  策略：用 (group数量, 已读长度) 追踪，而不是追踪 DOM 元素引用。
  //  因为 Vue 在流式渲染时可能替换内部 .chat-bubble 元素，
  //  导致元素级别的追踪失效。group数量 + 文本长度不受元素替换影响。
  // ===================================================================

  // 获取元素的可见文本
  // 克隆元素 → 移除 thinking/tool/内部区块 → 取纯文本
  // 这样无论 thinking 块显示还是隐藏，取到的文本都是一致的
  function _getVisibleText(el) {
    const clone = el.cloneNode(true);
    const strip = [
      '[class*="thinking"]',        // 推理过程块（任何包含 "thinking" 的类名）
      '.chat-reading-indicator',    // "正在思考..." 动画点
      '.chat-tool-msg-body',        // 工具调用结果块
      'details',                    // 折叠/展开的 details 元素
      '.chat-group-footer',         // 消息组底部（发送者名 + 时间）
      '.chat-bubble-actions',       // 气泡操作按钮
      '.chat-sender-name',          // 发送者名称
    ];
    for (const sel of strip) {
      clone.querySelectorAll(sel).forEach(c => c.remove());
    }
    return (clone.textContent || '').trim();
  }

  // 追踪状态
  let lastGroupCount = 0;  // 上一次看到的 .chat-group.assistant 数量
  let lastReadLen = 0;     // 上一次已读的文本长度（字符数）

  // 检查是否有新的 AI 回复文本需要朗读
  function checkAndRead() {
    // 查找页面上所有 assistant 消息组
    const groups = document.querySelectorAll('.chat-group.assistant');
    if (groups.length === 0) return;

    // 取最后一个（最新的）assistant 组，获取可见文本
    const lastGroup = groups[groups.length - 1];
    const fullText = _getVisibleText(lastGroup);
    if (!fullText) return;

    // 消息组数量增加了 → 新的 AI 回复 → 重置读位
    if (groups.length > lastGroupCount) {
      lastGroupCount = groups.length;
      lastReadLen = 0;
    }

    // 文本未增长或变短了（thinking 折叠等情况）→ 跳过
    if (fullText.length <= lastReadLen) return;

    // 只取新增部分（delta），实现流式递增朗读
    const delta = fullText.slice(lastReadLen).trim();
    lastReadLen = fullText.length;
    if (delta) {
      log('TTS delta:', delta.slice(0, 80));
      enqueueTTS(delta);
    }
  }

  // 启动 MutationObserver 监听聊天区域的 DOM 变化
  function startObserving() {
    // 找到包含所有 chat-group 的滚动容器
    // .chat-group-messages 的父级是 .chat-group，再上一级是滚动区域
    const container = document.querySelector('.chat-group-messages')?.parentElement?.parentElement
      || document.querySelector('.chat-main')
      || document.body;

    // 任何 DOM 变动（子元素添加/删除、文本变化）都触发 500ms 防抖检测
    const observer = new MutationObserver(() => {
      if (!ttsEnabled) return;
      if (debounceTimer) clearTimeout(debounceTimer);
      debounceTimer = setTimeout(checkAndRead, 500);
    });

    observer.observe(container, { childList: true, subtree: true, characterData: true });
    log('Observing messages in', container.tagName, container.className || '');
  }

  // ===================================================================
  //  键盘快捷键
  //  F6 或 Ctrl+Shift+M = 切换麦克风开关
  // ===================================================================
  document.addEventListener('keydown', (e) => {
    if (e.key === 'F6' || (e.ctrlKey && e.shiftKey && e.key === 'M')) {
      e.preventDefault();
      if (!recognition) initSTT();
      if (isRecording) stopRecording(); else startRecording();
    }
  });

  // ===================================================================
  //  页面可见性监听 — 切后台回来后恢复 TTS
  //  浏览器会在页面不可见时挂起 speechSynthesis，回来后不会自动恢复
  // ===================================================================
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible') {
      // 用 pause+resume trick 唤醒被 Chrome 挂起的 speechSynthesis
      if (window.speechSynthesis) {
        window.speechSynthesis.pause();
        window.speechSynthesis.resume();
      }
      // 如果 TTS 应该在工作但卡住了，重新推进队列
      if (ttsEnabled && speechQueue.length > 0 && !isSpeaking) {
        log('Page visible — restarting TTS queue');
        processSpeechQueue();
      }
    }
  });

  // ===================================================================
  //  初始化
  //  1. 等待 Control UI (Vue SPA) 渲染完毕
  //  2. 注入语音控制面板
  //  3. 启动 AI 消息监测
  //  4. 预加载语音合成音色
  // ===================================================================
  async function init() {
    log('Starting...');

    // 等待聊天输入框出现（最长等 25 秒，确保 Vue 渲染完成）
    try {
      await waitFor('.chat-compose__field textarea, .agent-chat__input textarea, textarea', 25000);
    } catch (_) {
      log('Timeout waiting for input, continuing anyway...');
    }

    // 额外等 2 秒确保 Vue 路由全部渲染完成
    await new Promise(r => setTimeout(r, 2000));

    injectToolbar();
    startObserving();

    // 预加载浏览器语音合成音色列表
    if (window.speechSynthesis) {
      window.speechSynthesis.getVoices();
      window.speechSynthesis.onvoiceschanged = () => window.speechSynthesis.getVoices();
    }

    log('Ready! F6 or Ctrl+Shift+M to toggle mic.');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

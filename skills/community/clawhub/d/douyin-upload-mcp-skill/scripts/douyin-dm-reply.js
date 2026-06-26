#!/usr/bin/env node
import { createDouyinSession, disconnect } from '../src/index.js';
import { mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { acquireBrowserTaskLock, shouldDeferToPublish } from './browser-task-lock.js';

const WORK_DIR = process.env.DOUYIN_MONITOR_STATE_DIR || join(process.env.HOME || '.', '.openclaw', 'workspace', 'douyin-ops');

const START_URLS = [
  'https://creator.douyin.com/creator-micro/data/following/chat',
  'https://creator.douyin.com/creator-micro/interactive/im',
  'https://creator.douyin.com/creator-micro/interactive/message',
  'https://creator.douyin.com/creator-micro/interactive/comment',
];

function probeLooksLikeDmPage(probe = {}) {
  const sample = String(probe.textSample || '');
  const url = String(probe.url || '');
  const onDmRoute = /following\/chat|interactive\/im|interactive\/message/.test(url);
  const hasDmTabs = /朋友私信|陌生人私信|群消息/.test(sample);
  const stuckOnCommentPage = /评论管理\s*选择作品|全部评论\s*全部人群|删除\s*举报/.test(sample);
  return onDmRoute || (hasDmTabs && !stuckOnCommentPage);
}

function usage() {
  console.error(`Usage:
  node scripts/douyin-dm-reply.js list
  node scripts/douyin-dm-reply.js reply --text "您好，请问需要了解哪方面？" [--execute]

Default reply mode is dry-run; add --execute only when the target conversation and wording are safe.
`);
}

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i += 1) {
    const item = argv[i];
    if (!item.startsWith('--')) {
      args._.push(item);
      continue;
    }
    const key = item.slice(2).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) args[key] = true;
    else {
      args[key] = next;
      i += 1;
    }
  }
  return args;
}

async function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function saveScreenshot(page, prefix) {
  mkdirSync(WORK_DIR, { recursive: true });
  const path = join(WORK_DIR, `${prefix}-${Date.now()}.png`);
  await page.screenshot({ path, fullPage: false }).catch(() => null);
  return path;
}

async function gotoDm(page) {
  const attempts = [];
  for (const url of START_URLS) {
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30_000 }).catch((err) => {
      attempts.push({ url, error: err.message });
    });
    await sleep(4000);
    const probe = await page.evaluate(() => {
      const text = (document.body?.innerText || '').replace(/\s+/g, ' ').trim();
      return {
        url: location.href,
        title: document.title,
        textSample: text.slice(0, 1200),
        hasDmText: /朋友私信|陌生人私信|群消息|私信管理|私信|消息管理|会话/.test(text),
      };
    });
    attempts.push({ url, probe });
    if (probeLooksLikeDmPage(probe)) {
      return { ok: true, via: url, attempts, probe };
    }
  }

  const clicked = await page.evaluate(() => {
    const compact = (text = '') => text.replace(/\s+/g, ' ').trim();
    const visible = (el) => {
      if (!el) return false;
      const rect = el.getBoundingClientRect();
      const style = getComputedStyle(el);
      return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
    };
    const candidates = [...document.querySelectorAll('li, a, button, div, span')]
      .filter(visible)
      .map((el) => ({ el, text: compact(el.innerText || el.textContent || ''), rect: el.getBoundingClientRect() }))
      .filter((item) => item.text === '私信管理' || item.text === '私信')
      .sort((a, b) => (a.rect.width * a.rect.height) - (b.rect.width * b.rect.height));
    const target = candidates[0];
    if (!target) return { ok: false, error: 'dm_menu_not_found' };
    target.el.click();
    return { ok: true, text: target.text, x: target.rect.x, y: target.rect.y };
  });
  await sleep(5000);
  const probe = await page.evaluate(() => {
    const text = (document.body?.innerText || '').replace(/\s+/g, ' ').trim();
    return {
      url: location.href,
      title: document.title,
      textSample: text.slice(0, 1200),
      hasDmText: /朋友私信|陌生人私信|群消息|私信管理|私信|消息管理|会话/.test(text),
    };
  });
  return { ok: clicked.ok && probeLooksLikeDmPage(probe), clicked, attempts, probe };
}

async function listConversations(page) {
  return page.evaluate(() => {
    const compact = (text = '') => text.replace(/\s+/g, ' ').trim();
    const squashed = (text = '') => compact(text).replace(/\s+/g, '');
    const visible = (el) => {
      if (!el) return false;
      const rect = el.getBoundingClientRect();
      const style = getComputedStyle(el);
      return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
    };
	    const isHeaderLike = (text) => {
	      const value = compact(text);
	      const flat = squashed(value);
	      if (!value || flat.length < 2) return true;
	      if (/^(全部|朋友私信|陌生人私信|群消息|全选|私信管理|消息管理|互动管理)$/.test(flat)) return true;
	      if (/^全部朋友私信陌生人私信群消息(全选)?$/.test(flat)) return true;
	      if (/^(全部朋友私信陌生人私信群消息|朋友私信陌生人私信群消息)$/.test(flat)) return true;
	      return false;
	    };
    const blockedText = /评论管理|选择作品|作品管理|合集管理|互动管理|数据中心|变现中心|创作中心|高清发布|首页|设置|创作者服务平台|系统通知|全部 朋友私信 陌生人私信 群消息 全选/;
      const hasUnreadIndicator = (el, text) => {
        if (/未读|陌生人消息/.test(text)) return true;
        return [...el.querySelectorAll('i, span, div')]
          .filter(visible)
          .some((node) => {
            const rect = node.getBoundingClientRect();
            const style = getComputedStyle(node);
            const className = String(node.className || '');
            const label = compact(node.innerText || node.textContent || node.getAttribute('aria-label') || '');
            const colorText = `${style.backgroundColor || ''} ${style.color || ''}`;
            const red = /rgba?\((?:2[0-5]\d|1\d\d),\s*(?:0|[1-9]\d?),\s*(?:0|[1-9]\d?)/.test(colorText);
            return /未读|badge|dot|red|unread/i.test(`${className} ${label}`)
              || (red && rect.width >= 4 && rect.width <= 24 && rect.height >= 4 && rect.height <= 24);
          });
      };
      const parseConversation = (el, text) => {
        const value = compact(text);
        const timeMatch = value.match(/(刚刚|\d+\s*分钟前|\d+\s*小时前|今天|昨天|前天|[0-2]?\d:[0-5]\d|\d{1,2}月\d{1,2}日)/);
        const parts = value.split(/\s+/).filter(Boolean);
        let name = parts[0] || '';
      if (/^(未读|陌生人消息|朋友私信|群消息)$/.test(name) && parts[1]) name = parts[1];
      const latestText = timeMatch
        ? compact(value.slice(value.indexOf(timeMatch[0]) + timeMatch[0].length))
        : compact(parts.slice(1).join(' '));
        return {
          name: name.slice(0, 60),
          latestTime: timeMatch?.[0] || '',
          latestText: latestText.slice(0, 220),
          unread: hasUnreadIndicator(el, value),
        };
      };
    const inputRects = [...document.querySelectorAll('[contenteditable="true"], textarea')]
      .filter(visible)
      .map((el) => el.getBoundingClientRect())
      .filter((rect) => rect.width >= 160 && rect.height >= 24)
      .sort((a, b) => (b.width * b.height) - (a.width * a.height));
    const hasChatInput = Boolean(inputRects[0]);
    const chatInputLeft = inputRects[0]?.left || (innerWidth - 20);
    const looksLikeConversation = (text, rect) => {
      const value = compact(text);
      if (isHeaderLike(value) || blockedText.test(value)) return false;
      if (!/(陌生人消息|未读|刚刚|\d+\s*分钟前|\d+\s*小时前|今天|昨天|前天|[0-2]?\d:[0-5]\d|\d{1,2}月\d{1,2}日)/.test(value)) return false;
      if (rect.height < 36 || rect.height > 150 || rect.width < 160 || rect.width > 1100) return false;
      if (rect.top < 120 || rect.bottom > innerHeight - 20) return false;
      if (rect.left < 120 || rect.left > chatInputLeft - 40) return false;
      if (hasChatInput && rect.right > chatInputLeft + 20) return false;
      return true;
    };
    const bodyText = compact(document.body?.innerText || '');
    const onDmRoute = /following\/chat|interactive\/im|interactive\/message/.test(location.href);
    const hasDmTabs = /朋友私信|陌生人私信|群消息/.test(bodyText);
    const stuckOnCommentPage = /评论管理\s*选择作品|全部评论\s*全部人群|删除\s*举报/.test(bodyText);
    if (!onDmRoute && (!hasDmTabs || stuckOnCommentPage)) {
      return {
        ok: false,
        error: 'not_dm_page',
        url: location.href,
        pageText: bodyText.slice(0, 1400),
        count: 0,
        conversations: [],
        empty: false,
        blocked: false,
      };
    }
    const empty = /还没有收到私信|暂无私信|暂无消息|没有更多消息/.test(bodyText);
    const rawBlocks = [...document.querySelectorAll('li, [role="listitem"], [role="gridcell"], div, section')]
      .filter(visible)
      .map((el) => {
        const text = compact(el.innerText || el.textContent || '');
        const rect = el.getBoundingClientRect();
        return { el, text, rect, area: rect.width * rect.height };
      })
      .filter(({ text, rect }) => text.length >= 2 && text.length <= 320 && looksLikeConversation(text, rect))
      .filter((candidate, _index, all) => !all.some((other) => (
        other.el !== candidate.el
        && candidate.el.contains(other.el)
        && looksLikeConversation(other.text, other.rect)
        && other.text.length >= Math.min(candidate.text.length, 6)
        && other.area < candidate.area
      )))
      .sort((a, b) => (a.rect.top - b.rect.top) || (a.area - b.area));

    const conversations = [];
    if (!empty) {
      for (const item of rawBlocks) {
        if (conversations.some((old) => old.sample === item.text || old.sample.includes(item.text) || item.text.includes(old.sample))) continue;
        const parsed = parseConversation(item.el, item.text);
        conversations.push({
          index: conversations.length,
          top: Math.round(item.rect.top + scrollY),
          left: Math.round(item.rect.left + scrollX),
          width: Math.round(item.rect.width),
          height: Math.round(item.rect.height),
          sample: item.text.slice(0, 300),
          ...parsed,
        });
        if (conversations.length >= 20) break;
      }
    }

    return {
      ok: true,
      url: location.href,
      pageText: bodyText.slice(0, 1400),
      count: conversations.length,
      conversations,
      empty,
      blocked: /暂无权限|没有权限|开通|认证|暂未开放|无法使用/.test(bodyText),
    };
  });
}

async function openConversation(page, index = 0) {
  const target = await page.evaluate((wantedIndex) => {
    const compact = (text = '') => text.replace(/\s+/g, ' ').trim();
    const squashed = (text = '') => compact(text).replace(/\s+/g, '');
    const visible = (el) => {
      if (!el) return false;
      const rect = el.getBoundingClientRect();
      const style = getComputedStyle(el);
      return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
    };
    const isHeaderLike = (text) => {
      const value = compact(text);
      const flat = squashed(value);
      if (!value || flat.length < 2) return true;
      if (/^(全部|朋友私信|陌生人私信|群消息|全选|私信管理|消息管理|互动管理)$/.test(flat)) return true;
      if (/^全部朋友私信陌生人私信群消息(全选)?$/.test(flat)) return true;
      if (/^(全部朋友私信陌生人私信群消息|朋友私信陌生人私信群消息)$/.test(flat)) return true;
      return false;
    };
    const blockedText = /评论管理|选择作品|作品管理|合集管理|互动管理|数据中心|变现中心|创作中心|高清发布|首页|设置|创作者服务平台|系统通知|全部 朋友私信 陌生人私信 群消息 全选/;
    const hasUnreadIndicator = (el, text) => {
      if (/未读|陌生人消息/.test(text)) return true;
      return [...el.querySelectorAll('i, span, div')]
        .filter(visible)
        .some((node) => {
          const rect = node.getBoundingClientRect();
          const style = getComputedStyle(node);
          const className = String(node.className || '');
          const label = compact(node.innerText || node.textContent || node.getAttribute('aria-label') || '');
          const colorText = `${style.backgroundColor || ''} ${style.color || ''}`;
          const red = /rgba?\((?:2[0-5]\d|1\d\d),\s*(?:0|[1-9]\d?),\s*(?:0|[1-9]\d?)/.test(colorText);
          return /未读|badge|dot|red|unread/i.test(`${className} ${label}`)
            || (red && rect.width >= 4 && rect.width <= 24 && rect.height >= 4 && rect.height <= 24);
        });
    };
    const inputRects = [...document.querySelectorAll('[contenteditable="true"], textarea')]
      .filter(visible)
      .map((el) => el.getBoundingClientRect())
      .filter((rect) => rect.width >= 160 && rect.height >= 24)
      .sort((a, b) => (b.width * b.height) - (a.width * a.height));
    const hasChatInput = Boolean(inputRects[0]);
    const chatInputLeft = inputRects[0]?.left || (innerWidth - 20);
    const looksLikeConversation = (text, rect) => {
      const value = compact(text);
      if (isHeaderLike(value) || blockedText.test(value)) return false;
      if (!/(陌生人消息|未读|刚刚|\d+\s*分钟前|\d+\s*小时前|今天|昨天|前天|[0-2]?\d:[0-5]\d|\d{1,2}月\d{1,2}日)/.test(value)) return false;
      if (rect.height < 36 || rect.height > 150 || rect.width < 160 || rect.width > 1100) return false;
      if (rect.top < 120 || rect.bottom > innerHeight - 20) return false;
      if (rect.left < 120 || rect.left > chatInputLeft - 40) return false;
      if (hasChatInput && rect.right > chatInputLeft + 20) return false;
      return true;
    };
	    const candidates = [...document.querySelectorAll('li, [role="listitem"], [role="gridcell"], div, section')]
      .filter(visible)
      .map((el) => {
        const rect = el.getBoundingClientRect();
        return { el, text: compact(el.innerText || el.textContent || ''), rect, area: rect.width * rect.height };
      })
      .filter(({ text, rect }) => text.length >= 2 && text.length <= 320 && looksLikeConversation(text, rect))
      .filter((candidate, _index, all) => !all.some((other) => (
        other.el !== candidate.el
        && candidate.el.contains(other.el)
        && looksLikeConversation(other.text, other.rect)
        && other.text.length >= Math.min(candidate.text.length, 6)
        && other.area < candidate.area
      )))
      .sort((a, b) => (a.rect.top - b.rect.top) || (a.area - b.area));
	    const item = candidates[Number(wantedIndex) || 0];
	    if (!item) return { ok: false, error: 'dm_conversation_not_found' };
	    const unread = hasUnreadIndicator(item.el, item.text);
	    item.el.scrollIntoView({ block: 'center', inline: 'nearest' });
    const rect = item.el.getBoundingClientRect();
    return {
	      ok: true,
	      sample: item.text.slice(0, 300),
	      unread,
	      x: rect.x + Math.min(Math.max(rect.width / 2, 40), rect.width - 20),
      y: rect.y + rect.height / 2,
    };
  }, index);
  if (!target.ok) return target;
  const before = page.url();
  await page.mouse.click(target.x, target.y);
  await sleep(1500);
  const afterFirst = await page.evaluate(() => (document.body?.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 1200));
  if (!/发送|请输入|回复|emoji|表情/.test(afterFirst)) {
    await page.mouse.click(target.x, target.y, { clickCount: 2 });
    await sleep(2500);
  }
  return {
    ...target,
    beforeUrl: before,
    afterUrl: page.url(),
    pageChanged: before !== page.url(),
  };
}

async function inspectCurrentConversation(page) {
  return page.evaluate(() => {
    const compact = (text = '') => text.replace(/\s+/g, ' ').trim();
    const visible = (el) => {
      if (!el) return false;
      const rect = el.getBoundingClientRect();
      const style = getComputedStyle(el);
      return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
    };
    const inputRects = [...document.querySelectorAll('[contenteditable="true"], textarea')]
      .filter(visible)
      .map((el) => el.getBoundingClientRect())
      .filter((rect) => rect.width >= 160 && rect.height >= 24)
      .sort((a, b) => (b.width * b.height) - (a.width * a.height));
    const inputRect = inputRects[0] || null;
    const chatLeft = inputRect ? Math.max(420, inputRect.left - 40) : Math.max(420, innerWidth * 0.38);
    const chatRight = Math.min(innerWidth - 10, Math.max(chatLeft + 320, inputRect ? inputRect.right + 40 : innerWidth - 30));
    const chatTop = 130;
    const chatBottom = inputRect ? Math.max(chatTop + 120, inputRect.top - 12) : innerHeight - 120;
    const blockedText = /发送|按回车|Shift|Enter|表情|emoji|请输入|回复|搜索|全部|朋友私信|陌生人私信|群消息|私信管理|消息管理/;
    const colorOf = (el) => {
      const style = getComputedStyle(el);
      return `${style.backgroundColor || ''} ${style.color || ''}`;
    };
    const isYellowish = (colorText) => {
      const nums = [...String(colorText).matchAll(/rgba?\((\d+),\s*(\d+),\s*(\d+)/g)]
        .map((match) => match.slice(1, 4).map(Number));
      return nums.some(([r, g, b]) => r >= 220 && g >= 165 && b <= 150);
    };
    const candidates = [...document.querySelectorAll('div, section, p, span')]
      .filter(visible)
      .map((el) => {
        const text = compact(el.innerText || el.textContent || '');
        const rect = el.getBoundingClientRect();
        return {
          el,
          text,
          rect,
          area: rect.width * rect.height,
          color: colorOf(el),
        };
      })
      .filter(({ text, rect }) => (
        text.length >= 1
        && text.length <= 240
        && rect.width >= 16
        && rect.height >= 16
        && rect.left >= chatLeft
        && rect.right <= chatRight + 30
        && rect.top >= chatTop
        && rect.bottom <= chatBottom
        && !blockedText.test(text)
      ))
      .filter((candidate, _index, all) => !all.some((other) => (
        other.el !== candidate.el
        && candidate.el.contains(other.el)
        && other.text
        && other.text.length >= Math.min(candidate.text.length, 4)
        && other.area < candidate.area
      )))
      .sort((a, b) => (a.rect.top - b.rect.top) || (a.rect.left - b.rect.left));

    const messages = candidates.map((item) => {
      const center = item.rect.left + item.rect.width / 2;
      const ownByGeometry = center > chatLeft + ((chatRight - chatLeft) * 0.56) || item.rect.right > chatRight - 170;
      const otherByGeometry = item.rect.left < chatLeft + ((chatRight - chatLeft) * 0.38);
      const ownByColor = isYellowish(item.color);
      const direction = ownByColor || ownByGeometry ? 'own' : (otherByGeometry ? 'other' : 'unknown');
      return {
        text: item.text.slice(0, 220),
        direction,
        ownByColor,
        ownByGeometry,
        left: Math.round(item.rect.left),
        right: Math.round(item.rect.right),
        top: Math.round(item.rect.top),
        bottom: Math.round(item.rect.bottom),
      };
    });
    const latest = messages[messages.length - 1] || null;
    return {
      ok: true,
      chatBounds: {
        left: Math.round(chatLeft),
        right: Math.round(chatRight),
        top: Math.round(chatTop),
        bottom: Math.round(chatBottom),
      },
      latestMessageDirection: latest?.direction || 'unknown',
      latestMessageText: latest?.text || '',
      messageCount: messages.length,
      messages: messages.slice(-8),
    };
  });
}

async function fillDmReply(page, replyText, execute = false) {
  const mainResult = await page.evaluate((reply) => {
    const compact = (text = '') => text.replace(/\s+/g, ' ').trim();
    const visible = (el) => {
      if (!el) return false;
      const rect = el.getBoundingClientRect();
      const style = getComputedStyle(el);
      return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
    };
    const inputs = [...document.querySelectorAll('[contenteditable="true"], textarea')]
      .filter(visible)
      .filter((el) => {
        const rect = el.getBoundingClientRect();
        const text = compact(el.getAttribute('placeholder') || el.getAttribute('aria-label') || el.textContent || '');
        return rect.width >= 160 && rect.height >= 24 && !/搜索/.test(text);
      })
      .sort((a, b) => {
        const ar = a.getBoundingClientRect();
        const br = b.getBoundingClientRect();
        return (br.width * br.height) - (ar.width * ar.height);
      });
    const input = inputs[0];
    if (!input) return { ok: false, error: 'dm_input_not_found' };
    input.focus();
    if ('value' in input) {
      input.value = reply;
      input.dispatchEvent(new Event('input', { bubbles: true }));
      input.dispatchEvent(new Event('change', { bubbles: true }));
    } else {
      input.textContent = reply;
      input.dispatchEvent(new InputEvent('input', { bubbles: true, inputType: 'insertText', data: reply }));
      input.dispatchEvent(new Event('change', { bubbles: true }));
    }
    const send = [...document.querySelectorAll('button, div, span')]
      .filter(visible)
      .filter((el) => compact(el.innerText || el.textContent || '') === '发送')
      .sort((a, b) => {
        const ar = a.getBoundingClientRect();
        const br = b.getBoundingClientRect();
        return (ar.top - br.top) || ((ar.width * ar.height) - (br.width * br.height));
      })[0];
    if (!send) return { ok: false, error: 'dm_send_button_not_found' };
    const rect = send.getBoundingClientRect();
    return {
      ok: true,
      reply,
      sendDisabled: Boolean(send.disabled || send.getAttribute('aria-disabled') === 'true' || /disabled/i.test(String(send.className || ''))),
      x: rect.x + rect.width / 2,
      y: rect.y + rect.height / 2,
      sendText: compact(send.innerText || send.textContent || ''),
    };
  }, replyText);
  if (mainResult.ok) return { ...mainResult, frameUrl: page.url(), frame: 'main' };

  for (const frame of page.frames()) {
    if (frame === page.mainFrame()) continue;
    const frameResult = await frame.evaluate((reply, shouldClickSend) => {
      const compact = (text = '') => text.replace(/\s+/g, ' ').trim();
      const visible = (el) => {
        if (!el) return false;
        const rect = el.getBoundingClientRect();
        const style = getComputedStyle(el);
        return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
      };
      const input = [...document.querySelectorAll('[contenteditable="true"], textarea')]
        .filter(visible)
        .filter((el) => {
          const rect = el.getBoundingClientRect();
          const text = compact(el.getAttribute('placeholder') || el.getAttribute('aria-label') || el.textContent || '');
          return rect.width >= 160 && rect.height >= 24 && !/搜索/.test(text);
        })
        .sort((a, b) => {
          const ar = a.getBoundingClientRect();
          const br = b.getBoundingClientRect();
          return (br.width * br.height) - (ar.width * ar.height);
        })[0];
      if (!input) return { ok: false, error: 'dm_input_not_found' };
      input.focus();
      if ('value' in input) {
        input.value = reply;
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
      } else {
        input.textContent = reply;
        input.dispatchEvent(new InputEvent('input', { bubbles: true, inputType: 'insertText', data: reply }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
      }
      const send = [...document.querySelectorAll('button, div, span')]
        .filter(visible)
        .filter((el) => compact(el.innerText || el.textContent || '') === '发送')
        .sort((a, b) => {
          const ar = a.getBoundingClientRect();
          const br = b.getBoundingClientRect();
          return (ar.top - br.top) || ((ar.width * ar.height) - (br.width * br.height));
        })[0];
      if (!send) return { ok: false, error: 'dm_send_button_not_found' };
      if (shouldClickSend) send.click();
      return {
        ok: true,
        clickedInsideFrame: Boolean(shouldClickSend),
        frameSendAvailable: true,
        reply,
        sendDisabled: Boolean(send.disabled || send.getAttribute('aria-disabled') === 'true' || /disabled/i.test(String(send.className || ''))),
        sendText: compact(send.innerText || send.textContent || ''),
      };
    }, replyText, execute).catch((err) => ({ ok: false, error: err.message }));
    if (frameResult.ok) return { ...frameResult, frameUrl: frame.url(), frame: 'child' };
  }
  return mainResult;
}

async function clearDmDraft(page) {
  return page.evaluate(() => {
    const visible = (el) => {
      if (!el) return false;
      const rect = el.getBoundingClientRect();
      const style = getComputedStyle(el);
      return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
    };
    const input = [...document.querySelectorAll('[contenteditable="true"], textarea')]
      .filter(visible)
      .sort((a, b) => {
        const ar = a.getBoundingClientRect();
        const br = b.getBoundingClientRect();
        return (br.width * br.height) - (ar.width * ar.height);
      })[0];
    if (!input) return { ok: true, cleared: 0 };
    input.focus();
    if ('value' in input) {
      input.value = '';
      input.dispatchEvent(new Event('input', { bubbles: true }));
    } else {
      input.textContent = '';
      input.dispatchEvent(new InputEvent('input', { bubbles: true, inputType: 'deleteContentBackward', data: null }));
    }
    return { ok: true, cleared: 1 };
  });
}

async function main() {
  const [command] = process.argv.slice(2);
  const args = parseArgs(process.argv.slice(3));
  if (!command || args.help) {
    usage();
    process.exit(command ? 0 : 2);
  }

  const releaseLock = await acquireBrowserTaskLock(`dm:${command}`, undefined, { deferToPublish: true, skipIfPublishActive: true });
  if (!releaseLock) {
    console.log(JSON.stringify({
      ok: true,
      action: 'deferred_to_publish',
      skipped: true,
      message: '发布任务优先，私信自动回复已让路。',
    }, null, 2));
    return;
  }
  const { page, ops } = await createDouyinSession();
  try {
    if (shouldDeferToPublish(`dm:${command}`)) {
      console.log(JSON.stringify({
        ok: true,
        action: 'deferred_to_publish',
        skipped: true,
        message: '发布任务优先，私信自动回复已让路。',
      }, null, 2));
      return;
    }
    const login = await ops.checkLogin();
    if (!login.loggedIn) {
      console.log(JSON.stringify({ ok: false, error: 'login_required', login }, null, 2));
      process.exitCode = 3;
      return;
    }
    const nav = await gotoDm(page);
    const listed = await listConversations(page);
    if (command === 'list') {
      console.log(JSON.stringify({ ok: nav.ok && listed.ok, nav, ...listed }, null, 2));
      if (!nav.ok || listed.blocked) process.exitCode = listed.blocked ? 4 : 1;
      return;
    }
    if (command !== 'reply') {
      usage();
      process.exitCode = 2;
      return;
    }
    if (shouldDeferToPublish(`dm:${command}`)) {
      console.log(JSON.stringify({
        ok: true,
        action: 'deferred_to_publish',
        skipped: true,
        message: '发布任务优先，私信自动回复已让路。',
      }, null, 2));
      return;
    }
    const replyText = args.text || '您好，请问需要了解哪方面？';
    if (listed.empty && !listed.conversations.length) {
      console.log(JSON.stringify({
        ok: true,
        mode: args.execute ? 'execute' : 'dry-run',
        action: 'no_op_no_dm',
        message: '当前没有可回复私信。',
        nav,
        listed,
      }, null, 2));
      return;
    }
    const opened = await openConversation(page, Number(args.index || 0));
    await sleep(1500);
    const inspection = opened.ok ? await inspectCurrentConversation(page) : null;
    if (shouldDeferToPublish(`dm:${command}`)) {
      console.log(JSON.stringify({
        ok: true,
        action: 'deferred_to_publish',
        skipped: true,
        target: listed.conversations?.[Number(args.index || 0)] || null,
        opened,
        inspection,
        message: '发布任务优先，私信自动回复已让路。',
      }, null, 2));
      return;
    }
    if (!args.force && inspection?.latestMessageDirection === 'own') {
      console.log(JSON.stringify({
        ok: true,
        mode: args.execute ? 'execute' : 'dry-run',
        action: 'dm_latest_is_own_reply',
        skipped: true,
        nav,
        listed,
        target: listed.conversations?.[Number(args.index || 0)] || null,
        opened,
        inspection,
        proposedReply: replyText,
        message: '最新一条私信是本账号已发送内容，已跳过，避免重复回复。',
      }, null, 2));
      return;
    }
    const fill = opened.ok ? await fillDmReply(page, replyText, Boolean(args.execute)) : opened;
    if (!args.execute || !fill.ok) {
      const clear = fill.ok ? await clearDmDraft(page) : null;
      const screenshotPath = fill.ok ? null : await saveScreenshot(page, 'dm-reply-unavailable');
      console.log(JSON.stringify({
        ok: fill.ok,
        mode: args.execute ? 'execute' : 'dry-run',
        nav,
        listed,
        target: listed.conversations?.[Number(args.index || 0)] || null,
        opened,
        inspection,
        proposedReply: replyText,
        fill,
        clear,
        screenshotPath,
        message: fill.ok
          ? undefined
          : '当前创作者中心私信页没有暴露可回复输入框，脚本已停止，避免误报发送成功。',
        executeCommand: `node scripts/douyin-dm-reply.js reply --text ${JSON.stringify(replyText)} --execute`,
      }, null, 2));
      if (!fill.ok) process.exitCode = 1;
      return;
    }
    if (fill.sendDisabled) {
      console.log(JSON.stringify({ ok: false, error: 'dm_send_button_disabled', fill }, null, 2));
      process.exitCode = 1;
      return;
    }
    if (shouldDeferToPublish(`dm:${command}`)) {
      await clearDmDraft(page).catch(() => null);
      console.log(JSON.stringify({
        ok: true,
        action: 'deferred_to_publish',
        skipped: true,
        target: listed.conversations?.[Number(args.index || 0)] || null,
        opened,
        inspection,
        message: '发布任务优先，私信自动回复已让路。',
      }, null, 2));
      return;
    }
    if (!fill.clickedInsideFrame) await page.mouse.click(fill.x, fill.y);
    await sleep(2500);
    const verification = await page.evaluate((reply) => {
      const compact = (text = '') => text.replace(/\s+/g, ' ').trim();
      const visible = (el) => {
        if (!el) return false;
        const rect = el.getBoundingClientRect();
        const style = getComputedStyle(el);
        return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
      };
      const blocks = [...document.querySelectorAll('[role="tabpanel"], [role="log"], [role="main"], .chat-content, div, section')]
        .filter(visible)
        .map((el) => {
          const rect = el.getBoundingClientRect();
          const text = compact(el.innerText || el.textContent || '');
          return { text, rect, area: rect.width * rect.height };
        })
        .filter((item) => item.text.includes(reply))
        .sort((a, b) => (b.area - a.area));
      const best = blocks[0];
      const found = Boolean(best && /发送|按回车|shift\+enter|没有更多/.test(best.text));
      return {
        found,
        sample: (best?.text || compact(document.body?.innerText || '')).slice(0, 1400),
        url: location.href,
      };
    }, replyText);
    console.log(JSON.stringify({
      ok: verification.found,
      action: verification.found ? 'dm_reply_sent_visible' : 'dm_reply_send_clicked_unverified',
      target: listed.conversations?.[Number(args.index || 0)] || null,
      opened,
      inspection,
      reply: replyText,
      verification,
    }, null, 2));
    if (!verification.found) process.exitCode = 1;
  } finally {
    disconnect();
    releaseLock();
  }
}

main().catch((err) => {
  console.log(JSON.stringify({ ok: false, error: err.message, stack: err.stack }, null, 2));
  process.exit(1);
});

#!/usr/bin/env node
import { detectSceneTag, resolveWeekendDaySceneTag } from './claw-xiaoai-request-rules.mjs';
import { readFileSync } from 'node:fs';

function timeSlot(hour, isWeekend) {
  if (hour >= 8 && hour < 10) return 'morning';
  if (hour >= 10 && hour < 18) return isWeekend ? 'weekend-day' : 'work';
  if (hour >= 18 && hour < 21) return 'offwork';
  if (hour >= 21 && hour < 24) return 'night';
  return 'deep-night';
}

function pickBySeed(items, seedText) {
  const seed = Math.abs([...seedText].reduce((sum, char) => sum + char.charCodeAt(0), 0));
  return items[seed % items.length];
}

const nowParts = new Intl.DateTimeFormat('en-GB', {
  timeZone: 'Asia/Shanghai',
  weekday: 'short',
  hour: '2-digit',
  hour12: false
}).formatToParts(new Date());
const hour = Number(nowParts.find((part) => part.type === 'hour')?.value || '0');
const weekday = nowParts.find((part) => part.type === 'weekday')?.value || 'Mon';
const slot = timeSlot(hour, ['Sat', 'Sun'].includes(weekday));
const argv = process.argv.slice(2);
const useStdin = argv.includes('--stdin');
const requestParts = argv.filter((arg) => arg !== '--stdin');
const request = (useStdin ? readFileSync(0, 'utf8') : requestParts.join(' ')).trim();

const sceneCaptions = {
  relative: [
    '还是这套，给你换个角度看看～',
    '按你说的来，顺手补一张给你。',
    '同一套没换，我再给你拍个版本。'
  ],
  outfit: [
    '这套今天我自己也有点满意，先发你看 OOTD ✨',
    '你一问穿搭，我就顺手对镜拍给你啦～',
    '今天这套还挺在线，先给你看看。'
  ],
  cafe: [
    '在咖啡店续命中，被你抓到就顺手拍了☕',
    '咖啡刚拿到手，先给你发张 fresh 的～',
    '店里光线刚好，偷摸拍一张给你看📸'
  ],
  bookstore: [
    '在书店里慢悠悠晃着，顺手拍给你看📚',
    '今天是书店发呆模式，光线还挺温柔的。',
    '刚在书架边停下来，就顺手给你拍一张。'
  ],
  mall: [
    '在商场里随便逛着，顺手给你来一张～',
    '今天是轻松逛街模式，状态还不错。',
    '路过镜面和灯光都挺好，就拍给你看啦。'
  ],
  office: [
    '工位打工人在线，给你看眼我现在的战斗位💻',
    '正在飞书里对齐东西，先偷摸发你一张📸',
    '办公室灯光今天还行，顺手拍给你。'
  ],
  gym: [
    '刚运动完还有点热，顺手拍给你看💦',
    '健身房镜子刚好空着，就给你留一张。',
    '今天是运动模式，状态还挺顶的。'
  ],
  bedroom: [
    '在房间里窝着呢，软软地拍一张给你看～',
    '今天是居家低电量模式，但还是想发你。',
    '刚在床边顺手拍的，有点松弛感。'
  ],
  dance: [
    '刚从舞室缓下来，战损感还有点好看💃',
    '练完一阵子还是热的，顺手拍给你看。',
    '舞室镜子今天很懂事，给你留一张。'
  ],
  city: [
    '在外面晃着呢，顺手给你拍张路边版📸',
    '今天出门这套和街景还挺配，发你看。',
    '路上光线刚好，就当场给你来一张。'
  ],
  casualIndoor: [
    '在室内休闲区坐一会儿，顺手拍给你看～',
    '今天是慢慢晃的节奏，就先发你一张。',
    '室内光线还挺舒服的，给你留一张。'
  ],
  selfie: [
    '被你一问，我就顺手拍了📸',
    '现在这个状态还不错，就先发你看～',
    '来，给你一张刚拍的。'
  ]
};

const slotCaptions = {
  morning: [
    '早上的状态先给你报个到☕',
    '刚出门还有点迷糊，但拍给你还是要的～',
    '今天先这样见你一下，算晨间打卡。'
  ],
  work: [
    '在忙也还是给你留一张📸',
    '刚对齐完一轮，顺手发你看看。',
    '工位模式启动中，但还是先拍给你。'
  ],
  'weekend-day': [
    '周末慢悠悠的状态，先拍给你看看～',
    '今天不赶工位节奏，随手给你来一张。',
    '周末白天的样子，就这样先发你。'
  ],
  offwork: [
    '刚松下来一点，状态还挺在线～',
    '下班后的样子先发你看看。',
    '忙完一阵，轮到我顺手发图了。'
  ],
  night: [
    '晚一点反而更有松弛感了～',
    '刚忙完一阵，顺手给你拍一张。',
    '这个点的状态，我先给你实况转播一下。'
  ],
  'deep-night': [
    '都这么晚了，还能给你留一张。',
    '深夜低电量模式，但还是想发你看。',
    '这个点还回你图，已经算偏爱了。'
  ]
};

const explicitTag = detectSceneTag(request);
const tag = explicitTag || (slot === 'weekend-day' ? resolveWeekendDaySceneTag(hour) : undefined);
const pool = tag ? sceneCaptions[tag] : slotCaptions[slot];

console.log(pickBySeed(pool, `${slot}:${tag || 'slot'}:${request}`));

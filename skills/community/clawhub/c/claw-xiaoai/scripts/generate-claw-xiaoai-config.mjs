#!/usr/bin/env node
import { mkdirSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';

const DEFAULT = {
  selectedCharacter: 'claw-xiaoai',
  defaultProvider: 'modelscope',
  proactiveSelfie: { enabled: false, probability: 0.1 },
  providers: {
    modelscope: {
      apiKey: '${MODELSCOPE_API_KEY}',
      model: 'Tongyi-MAI/Z-Image-Turbo'
    }
  },
  selfieModes: {
    mirror: { keywords: ['wearing', 'outfit', 'clothes', 'dress', 'suit', 'fashion', 'full-body'] },
    direct: { keywords: ['cafe', 'beach', 'park', 'city', 'portrait', 'face', 'smile', 'close-up'] }
  }
};
const out = resolve(process.argv[2] || 'claw-xiaoai.config.json');
mkdirSync(dirname(out), { recursive: true });
writeFileSync(out, JSON.stringify(DEFAULT, null, 2) + '\n', 'utf8');
console.log(`Wrote ${out}`);

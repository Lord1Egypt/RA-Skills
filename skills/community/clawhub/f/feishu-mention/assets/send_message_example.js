/**
 * Feishu Message Sending Example (v2.0)
 * 
 * Demonstrates how to prepare a message with @mentions using the resolver
 * and format it for the Feishu API.
 */

import { resolve } from '../index.js';

// Configuration
const ACCOUNT_ID = 'elves'; // The OpenClaw account ID
const CHAT_ID = 'oc_acc4410336517a2ff73413fac977c39a';

async function main() {
  console.log('===== Feishu Message Preparation Example =====\n');

  // 1. Prepare raw text with mentions
  const rawText = '你好 @product，请协助 @张三 查看问题';
  console.log(`📝 Raw Text: "${rawText}"`);

  // 2. Resolve mentions using OpenClaw config
  // This step converts "@product" -> "<at user_id='...'>product</at>"
  const resolvedText = await resolve(rawText, ACCOUNT_ID, CHAT_ID);
  console.log(`✨ Resolved Text: "${resolvedText}"\n`);

  // 3. Construct Feishu Message Objects
  
  // Option A: Text Message (Simple)
  // Note: <at> tags work in text messages too if user_id is correct
  const textMessage = {
    msg_type: 'text',
    content: JSON.stringify({
      text: resolvedText
    })
  };
  console.log('📦 Option A (Text Message):');
  console.log(JSON.stringify(textMessage, null, 2));

  // Option B: Post Message (Rich Text) - Recommended
  const postMessage = {
    msg_type: 'post',
    content: JSON.stringify({
      zh_cn: {
        title: 'System Notification',
        content: [
          [
            {
              tag: 'text',
              text: resolvedText // Feishu parses <at> tags in text content
            }
          ]
        ]
      }
    })
  };
  console.log('\n📦 Option B (Post Message):');
  console.log(JSON.stringify(postMessage, null, 2));

  // 4. (Mock) Send to API
  // await sendToFeishuApi(CHAT_ID, postMessage);
}

main().catch(console.error);

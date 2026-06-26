import { resolve } from './index.js';

async function runTest() {
  const text = '你好，欢迎 @product 进群';
  const accountId = 'elves';
  const chatId = 'oc_acc4410336517a2ff73413fac977c39a';

  console.log(`Input Text: "${text}"`);
  console.log(`Context: Account=${accountId}, ChatId=${chatId}`);

  // This will trigger the resolver to:
  // 1. Load config for 'elves' and 'product'
  // 2. Fetch bot info for 'product' (to get its open_id)
  // 3. Resolve @product -> <at user_id="...">@product</at>
  const result = await resolve(text, accountId, chatId);
  
  console.log('Result:', result);
}

runTest();

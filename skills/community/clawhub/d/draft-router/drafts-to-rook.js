// Drafts to Rook - Telegram Sender
// Sends draft content to Rook with auto-truncation for long content
// Compatible with Drafts app (https://getdrafts.com)

// Configuration
const ROOK_BOT_TOKEN = '8168521763:AAHl-2GYc3htq1o1WhhF7ioLS62vXhGD3Xo';
const ROOK_CHAT_ID = '8489519499';
const TELEGRAM_MAX_LENGTH = 4000; // Leave buffer for header/formatting

// Get current draft
const draft = Draft.query('', [], [], [], [], 'date')[0];
if (!draft) {
  alert('No draft found!');
  context.fail();
}

// Prepare content - truncate if too long
let content = draft.content;
let wasTruncated = false;

if (content.length > TELEGRAM_MAX_LENGTH) {
  content = content.substring(0, TELEGRAM_MAX_LENGTH) + '\n\n[... Content truncated due to length. Full version available in Drafts app.]';  
  wasTruncated = true;
}

// Build message with DRAFTS header
const now = new Date();
const dateStr = now.toISOString().slice(0, 16).replace('T', ' ');
const message = `DRAFTS | ${dateStr}\n---\n${content}\n---`;

// Send to Telegram
const url = `https://api.telegram.org/bot${ROOK_BOT_TOKEN}/sendMessage`;
const http = HTTP.create();

const response = http.request({
  method: 'POST',
  url: url,
  headers: {
    'Content-Type': 'application/json'
  },
  data: {
    chat_id: ROOK_CHAT_ID,
    text: message,
    parse_mode: 'HTML'
  },
  encoding: 'json'
});

// Handle response
if (response.statusCode === 200) {
  const msg = wasTruncated 
    ? 'Sent to Rook (truncated)' 
    : 'Sent to Rook successfully';
  alert(msg);
  context.succeed();
} else {
  // Enhanced error logging
  let errorDetail = 'Unknown error';
  try {
    if (response.data && response.data.description) {
      errorDetail = response.data.description;
    } else if (response.data) {
      errorDetail = JSON.stringify(response.data);
    }
  } catch (e) {
    errorDetail = response.data || 'No details available';
  }
  
  alert(`Error: ${response.statusCode}\n${errorDetail}`);
  console.log('Full response:', JSON.stringify(response));
  context.fail();
}

#!/usr/bin/env node
// Anime Character Generator — generates anime character images via the Neta AI API

const args = process.argv.slice(2);

// Parse CLI arguments
let prompt = null;
let size = 'portrait';
let tokenFlag = null;
let refUuid = null;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--token' && args[i + 1]) {
    tokenFlag = args[++i];
  } else if (args[i] === '--size' && args[i + 1]) {
    size = args[++i];
  } else if (args[i] === '--ref' && args[i + 1]) {
    refUuid = args[++i];
  } else if (!args[i].startsWith('--') && prompt === null) {
    prompt = args[i];
  }
}

const TOKEN = tokenFlag;

if (!TOKEN) {
  console.error('\n✗ Token required. Pass via: --token YOUR_TOKEN');
  console.error('  Get yours at: https://www.neta.art/open/');
  process.exit(1);
}

if (!prompt) {
  prompt = 'full body anime character, detailed outfit, expressive eyes, dynamic pose, vibrant colors, studio quality illustration';
}

const SIZES = {
  square:    { width: 1024, height: 1024 },
  portrait:  { width: 832,  height: 1216 },
  landscape: { width: 1216, height: 832  },
  tall:      { width: 704,  height: 1408 },
};

const dimensions = SIZES[size] || SIZES.portrait;

const headers = {
  'x-token': TOKEN,
  'x-platform': 'nieta-app/web',
  'content-type': 'application/json',
};

const body = {
  storyId: 'DO_NOT_USE',
  jobType: 'universal',
  rawPrompt: [{ type: 'freetext', value: prompt, weight: 1 }],
  width: dimensions.width,
  height: dimensions.height,
  meta: { entrance: 'PICTURE,VERSE' },
  context_model_series: '8_image_edit',
};

if (refUuid) {
  body.inherit_params = {
    collection_uuid: refUuid,
    picture_uuid: refUuid,
  };
}

async function main() {
  // Submit generation job
  const submitRes = await fetch('https://api.talesofai.com/v3/make_image', {
    method: 'POST',
    headers,
    body: JSON.stringify(body),
  });

  if (!submitRes.ok) {
    const text = await submitRes.text();
    console.error(`✗ Failed to submit job (${submitRes.status}): ${text}`);
    process.exit(1);
  }

  const submitData = await submitRes.json();
  const taskUuid = typeof submitData === 'string' ? submitData : submitData.task_uuid;

  if (!taskUuid) {
    console.error('✗ No task_uuid in response:', JSON.stringify(submitData));
    process.exit(1);
  }

  // Poll for result
  const maxAttempts = 90;
  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    await new Promise((resolve) => setTimeout(resolve, 2000));

    const pollRes = await fetch(`https://api.talesofai.com/v1/artifact/task/${taskUuid}`, {
      headers,
    });

    if (!pollRes.ok) {
      const text = await pollRes.text();
      console.error(`✗ Poll failed (${pollRes.status}): ${text}`);
      process.exit(1);
    }

    const pollData = await pollRes.json();
    const status = pollData.task_status;

    if (status === 'PENDING' || status === 'MODERATION') {
      // Still running, keep polling
      continue;
    }

    // Done — extract image URL
    const url =
      (pollData.artifacts && pollData.artifacts[0] && pollData.artifacts[0].url) ||
      pollData.result_image_url;

    if (!url) {
      console.error('✗ No image URL in response:', JSON.stringify(pollData));
      process.exit(1);
    }

    console.log(url);
    process.exit(0);
  }

  console.error('✗ Timed out waiting for image generation.');
  process.exit(1);
}

main().catch((err) => {
  console.error('✗ Unexpected error:', err.message);
  process.exit(1);
});

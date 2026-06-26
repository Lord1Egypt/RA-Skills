#!/usr/bin/env node

import { httpsRequest, getApiKey, routerMultimodalUrl, truncateBody } from './utils.mjs';
import { imageToDataUri, isLocalFilePath } from './types.mjs';
import { fileURLToPath } from 'url';

/**
 * Call multimodal router for direct inference using internal API.
 * @param {string} text - User's text query
 * @param {string} imageUrl - URL or local file path to the image (optional)
 * @returns {Promise<Object>} API response
 */
export async function callMultimodal(text, imageUrl) {
  const apiKey = getApiKey();
  const messages = [
    {
      role: 'user',
      content: [
        {
          type: 'text',
          text: text
        }
      ]
    }
  ];

  // Add image if provided
  if (imageUrl) {
    // Convert local file path to data URI
    const resolvedUrl = isLocalFilePath(imageUrl) ? imageToDataUri(imageUrl) : imageUrl;
    messages[0].content.push({
      type: 'image_url',
      image_url: {
        url: resolvedUrl
      }
    });
  }

  const requestBody = {
    messages
  };

  const response = await httpsRequest(routerMultimodalUrl(), {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
    body: JSON.stringify(requestBody),
  });

  if (response.statusCode !== 200) {
    throw new Error(`Multimodal call failed with status ${response.statusCode}: ${truncateBody(response.body)}`);
  }

  let result;
  try {
    result = JSON.parse(response.body);
  } catch (err) {
    throw new Error(`Failed to parse multimodal response: ${err.message}`);
  }

  return result;
}

/**
 * CLI entry point for testing multimodal functionality.
 */
async function main() {
  const text = process.argv[2];
  const imageUrl = process.argv[3];

  if (!text) {
    console.error('Usage: node multimodal.mjs <text> [image-url]');
    console.error('Example: node multimodal.mjs "图片里有什么"');
    console.error('Example: node multimodal.mjs "图片里有什么" "http://example.com/image.jpg"');
    process.exit(1);
  }

  try {
    const result = await callMultimodal(text, imageUrl);
    const sanitizedImageUrl = imageUrl && !isLocalFilePath(imageUrl) ? imageUrl : (imageUrl ? '<local-file>' : null);
    console.log(JSON.stringify({
      success: true,
      text,
      imageUrl: sanitizedImageUrl,
      result
    }, null, 2));
  } catch (err) {
    console.error(JSON.stringify({
      success: false,
      error: err.message
    }, null, 2));
    process.exit(1);
  }
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  main();
}

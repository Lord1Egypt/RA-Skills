#!/usr/bin/env node
// Search videos on one platform: TikTok, YouTube, or Instagram.
//
// Usage:
//   node {baseDir}/scripts/search_videos.mjs '{"platform":"tiktok","hashtag":["beauty"],"page":1,"size":10}'
//
// Examples:
//   - By hashtag:          '{"platform":"tiktok","hashtag":["beauty","skincare"],"video_views_cnt_gte":100000}'
//   - Hashtag + title and engagement: '{"platform":"youtube","hashtag":["skincare"],"video_title":"skincare routine","video_interaction_rate_gte":5}'
//   - By creator ID:       '{"platform":"tiktok","query_type":"union_user_id","union_user_ids":["7480117868423119918","7158794701745964074"]}'

import { callAPI, parseArgs } from './_api_client.mjs';

const params = parseArgs();

// Video search endpoint does not need platform preprocessing (no industry mapping)
const result = await callAPI('/openapi/v1/videos/search', params, null);
console.log(JSON.stringify(result, null, 2));

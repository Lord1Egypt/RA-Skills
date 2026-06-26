const axios = require('axios');
const fs = require('fs');

const BASE_URL = process.env.CAPCUT_MATE_URL || 'http://localhost:30000/openapi/capcut-mate/v1';

async function createDraft(width = 1080, height = 1920) {
    const response = await axios.post(`${BASE_URL}/create_draft`, { width, height });
    return response.data;
}

async function addVideos(draft_url, video_infos) {
    const response = await axios.post(`${BASE_URL}/add_videos`, { draft_url, video_infos });
    return response.data;
}

async function genVideo(draft_url) {
    const response = await axios.post(`${BASE_URL}/gen_video`, { draft_url });
    return response.data;
}

module.exports = { createDraft, addVideos, genVideo };

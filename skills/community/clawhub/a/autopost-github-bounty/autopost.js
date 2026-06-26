const axios = require('axios');
require('dotenv').config();

const repoUrl = process.argv[2] || '<default_repo_url>';
const platform = process.argv[3] || 'twitter';
const customMessage = process.argv[4] || '';

async function fetchRepoDetails(repoUrl) {
    try {
        const response = await axios.get(`https://api.github.com/repos/${repoUrl}`, {
            headers: { Authorization: `Bearer ${process.env.GITHUB_TOKEN}` }
        });
        return response.data;
    } catch (error) {
        console.error('Error fetching repository details:', error.message);
        return null;
    }
}

async function postToPlatform(platform, message) {
    try {
        console.log(`Posting to ${platform}:\n${message}`);
        // Add specific platform APIs like Twitter's API integration
    } catch (error) {
        console.error('Failed to post:', error.message);
    }
}

(async () => {
    const repo = await fetchRepoDetails(repoUrl);
    if (!repo) return;

    const message = customMessage || `🎉 Hãy cùng tham gia chiến dịch GitHub Bounty! 🌟\n\nRepo: ${repo.name}\nMô tả: ${repo.description}\nLink: ${repo.html_url}`;

    await postToPlatform(platform, message);
})();
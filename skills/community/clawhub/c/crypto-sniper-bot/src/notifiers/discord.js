const axios = require('axios');

/**
 * Discord Notifier
 */
class DiscordNotifier {
  constructor(webhookUrl) {
    this.webhookUrl = webhookUrl;
  }

  /**
   * Send trending report to Discord
   * @param {Array} repos - Trending repositories
   * @param {object} options - Additional options
   */
  async sendTrendingReport(repos, options = {}) {
    if (!this.webhookUrl) {
      console.warn('Discord webhook not configured');
      return false;
    }

    const embeds = this.createEmbeds(repos, options);

    try {
      await axios.post(this.webhookUrl, {
        username: 'GitHub Trending Monitor',
        embeds
      });
      return true;
    } catch (error) {
      console.error('Discord send failed:', error.message);
      return false;
    }
  }

  /**
   * Create Discord embed messages
   */
  createEmbeds(repos, options = {}) {
    const { language = 'All', since = 'daily' } = options;
    const timeLabel = { daily: 'Today', weekly: 'This Week', monthly: 'This Month' }[since] || 'Today';
    const embeds = [];

    // Header embed
    embeds.push({
      title: `🔥 GitHub Trending - ${timeLabel}`,
      description: language && language !== 'all' ? `Language: **${language}**` : 'All Languages',
      color: 0xff6b35,
      timestamp: new Date().toISOString(),
      footer: { text: 'GitHub Trending Monitor' }
    });

    if (!repos || repos.length === 0) {
      embeds.push({
        description: '❌ No trending repositories found.',
        color: 0xff0000
      });
      return embeds;
    }

    // Repository embeds (max 10)
    repos.slice(0, 10).forEach((repo, index) => {
      const fields = [
        { name: '⭐ Stars', value: repo.stars.toLocaleString(), inline: true },
        { name: '🍴 Forks', value: repo.forks.toLocaleString(), inline: true }
      ];

      if (repo.todayStars > 0) {
        fields.push({ name: '📈 Today', value: `+${repo.todayStars}`, inline: true });
      }

      if (repo.language) {
        fields.push({ name: '💻 Language', value: repo.language, inline: true });
      }

      embeds.push({
        title: `${index + 1}. ${repo.fullName}`,
        description: repo.description || 'No description provided.',
        url: repo.url,
        color: 0x0366d6,
        fields
      });
    });

    return embeds;
  }
}

module.exports = DiscordNotifier;

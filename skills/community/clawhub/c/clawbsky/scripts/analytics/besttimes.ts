/**
 * Best Post Times Module
 * AI suggests optimal posting times using local LLM + historical data
 */

import { getOllamaClient } from '../llm.js';
import { getDailyStats, getFollowerHistory } from './engagement.js';

/**
 * Analyze posting patterns and suggest best times
 */
export async function suggestBestPostTimes(): Promise<{
  recommendations: { day: string; time: string; score: number; reason: string }[];
  timezone: string;
}> {
  const ollama = getOllamaClient();
  
  // Get historical data
  const dailyStats = getDailyStats(30);
  const followerHistory = getFollowerHistory(30);
  
  // Analyze patterns
  const prompt = `Given this historical engagement data, suggest the 3 best times to post on Bluesky.
Return as JSON:
{
  "recommendations": [
    {"day": "Monday", "time": "9:00 AM", "score": 95, "reason": "High engagement from weekdays"},
    ...
  ],
  "timezone": "UTC"
}

Historical data:
- Posts per day: ${JSON.stringify(dailyStats.map(s => ({ date: s.date, posts: s.posts, likes: s.likesGiven })))}
- Follower count history: ${JSON.stringify(followerHistory.map(f => ({ date: f.recordedAt, count: f.count })))}`;

  try {
    const response = await ollama.chat({
      model: 'qwen3.5:4b',
      messages: [{ role: 'user', content: prompt }],
      format: 'json'
    });

    return JSON.parse(response.message.content);
  } catch (error) {
    // Fallback recommendations
    return {
      recommendations: [
        { day: 'Tuesday', time: '9:00 AM', score: 85, reason: 'Generally high weekday engagement' },
        { day: 'Wednesday', time: '12:00 PM', score: 80, reason: 'Lunchtime engagement spike' },
        { day: 'Thursday', time: '6:00 PM', score: 75, reason: 'Evening user activity' }
      ],
      timezone: 'UTC'
    };
  }
}

/**
 * Get engagement heatmap data
 */
export function getEngagementHeatmap(): { hour: number; day: number; avgEngagement: number }[] {
  // This would require more granular tracking
  // For now, return placeholder data
  const heatmap = [];
  
  for (let day = 0; day < 7; day++) {
    for (let hour = 0; hour < 24; hour++) {
      // Placeholder - real implementation would track individual post times
      const baseEngagement = hour >= 9 && hour <= 18 ? 50 : 25;
      const dayBonus = day >= 1 && day <= 4 ? 20 : 0; // Weekdays better
      
      heatmap.push({
        hour,
        day,
        avgEngagement: baseEngagement + dayBonus + Math.random() * 20
      });
    }
  }
  
  return heatmap;
}

/**
 * Calculate optimal post frequency
 */
export async function suggestPostFrequency(): Promise<{
  dailyPosts: number;
  weeklyPosts: number;
  reason: string;
}> {
  const ollama = getOllamaClient();
  
  const stats = getDailyStats(30);
  const followerGrowth = getFollowerHistory(30);
  
  const prompt = `Based on this data, suggest optimal posting frequency.
Return as JSON:
{
  "dailyPosts": 3,
  "weeklyPosts": 15,
  "reason": "Your audience is most active on weekdays..."
}

Data:
- Daily stats: ${JSON.stringify(stats)}
- Follower growth: ${followerGrowth.length} data points`;

  try {
    const response = await ollama.chat({
      model: 'qwen3.5:4b',
      messages: [{ role: 'user', content: prompt }],
      format: 'json'
    });

    return JSON.parse(response.message.content);
  } catch {
    return {
      dailyPosts: 3,
      weeklyPosts: 15,
      reason: 'General recommendation: 1-5 posts per day optimal for growth'
    };
  }
}
/**
 * Farcaster Cast Integration
 *
 * Share Identity Card and supported projects on Farcaster
 */

import { PersonalityType } from '../types/personality';

export interface CastContent {
  userId: string;
  personalityType: PersonalityType;
  tokenId: number;
  supportedProjects: string[];
  nftImageUrl: string;
}

export class FarcasterCast {
  /**
   * Share Identity Card results on Farcaster
   */
  async share(content: CastContent): Promise<string> {
    console.log(`📢 Sharing on Farcaster...`);

    const castText = this.formatCastText(content);

    // TODO: Integrate with Farcaster API
    // For hackathon demo, simulate cast
    const castUrl = await this.simulateCast(castText, content.nftImageUrl);

    console.log(`✅ Cast published: ${castUrl}`);

    return castUrl;
  }

  /**
   * Format cast text
   */
  private formatCastText(content: CastContent): string {
    const emoji = this.getPersonalityEmoji(content.personalityType);

    return `
${emoji} Just discovered my Bloom Identity: ${content.personalityType}!

My AI Agent analyzed my on-chain & social activity, minted my Supporter Identity Card (SBT), and auto-supported ${content.supportedProjects.length} matching projects 🚀

Powered by @bloom @openclaw on @base

🔗 View my card: https://bloomprotocol.ai/identity/${content.tokenId}
    `.trim();
  }

  /**
   * Get emoji for personality type
   */
  private getPersonalityEmoji(type: PersonalityType): string {
    const emojiMap = {
      [PersonalityType.THE_VISIONARY]: '💜',
      [PersonalityType.THE_EXPLORER]: '💚',
      [PersonalityType.THE_CULTIVATOR]: '🩵',
      [PersonalityType.THE_OPTIMIZER]: '🧡',
      [PersonalityType.THE_INNOVATOR]: '💙',
    };
    return emojiMap[type] || '🎴';
  }

  /**
   * Simulate cast publication
   */
  private async simulateCast(text: string, imageUrl: string): Promise<string> {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 500));

    // Return mock Warpcast URL
    const castHash = Math.random().toString(36).substr(2, 9);
    return `https://warpcast.com/bloom/${castHash}`;
  }
}

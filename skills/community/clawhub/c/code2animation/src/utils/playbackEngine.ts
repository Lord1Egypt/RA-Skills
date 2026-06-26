import { TransitionKind } from '@/types';

/**
 * Simplified Playback Engine - Pre-calculated timeline
 */

export interface MediaItem {
  id: string;
  src: string;
  startTime: number;
  endTime: number;
  duration: number;
  words: string;
  clipIndex: number;
  mediaIndex: number;
  transitionIn?: TransitionKind;
  transitionDuration?: number;
  stayInClip?: boolean;
  clipStartTime: number;
  clipEndTime: number;
}

export interface PlaybackTimeline {
  mediaItems: MediaItem[];
  totalDuration: number;
  clipDurations: number[];
  clipStartTimes: number[];
}

export interface WordBoundary {
  text: string;
  startTime: number; // in seconds
  duration: number;  // in seconds
}

/**
 * Load and parse word boundaries from audio JSON file
 */
async function loadWordBoundaries(projectName: string, clipIndex: number): Promise<WordBoundary[]> {
  try {
    const response = await fetch(`/projects/${projectName}/audio/${clipIndex}.json`);
    const data = await response.json();
    
    return data.map((item: any) => {
      const wordData = item.Metadata[0].Data;
      return {
        text: wordData.text.Text,
        startTime: wordData.Offset / 10000000, // Convert from 100ns to seconds
        duration: wordData.Duration / 10000000
      };
    });
  } catch (error) {
    console.warn(`Failed to load word boundaries for clip ${clipIndex}:`, error);
    return [];
  }
}

/**
 * Find the start time of a word or phrase in word boundaries
 */
function findWordStartTime(wordBoundaries: WordBoundary[], targetWords: string): number {
  if (!targetWords || wordBoundaries.length === 0) return 0;
  
  const words = targetWords.trim().split(/\s+/);
  const firstWord = words[0].toLowerCase().replace(/[^a-z0-9]/g, '');
  
  const boundary = wordBoundaries.find(wb => 
    wb.text.toLowerCase().replace(/[^a-z0-9]/g, '') === firstWord
  );
  
  return boundary ? boundary.startTime : 0;
}

/**
 * Get total duration from word boundaries
 */
function getClipDurationFromBoundaries(wordBoundaries: WordBoundary[]): number {
  if (wordBoundaries.length === 0) return 2; // fallback
  
  const lastBoundary = wordBoundaries[wordBoundaries.length - 1];
  return lastBoundary.startTime + lastBoundary.duration;
}

/**
 * Pre-calculate complete timeline with all media items and their exact timing
 */
export async function calculateCompleteTimeline(project: any): Promise<PlaybackTimeline> {
  const projectName = project.name;
  const basePath = `/projects/${projectName}/footage`;
  const mediaItems: MediaItem[] = [];
  const clipDurations: number[] = [];
  const clipStartTimes: number[] = [];
  
  let globalTime = 0;
  
  // Load all word boundaries first
  const allWordBoundaries: WordBoundary[][] = [];
  for (let clipIndex = 0; clipIndex < project.clips.length; clipIndex++) {
    const wordBoundaries = await loadWordBoundaries(projectName, clipIndex);
    allWordBoundaries.push(wordBoundaries);
  }
  
  // Process each clip with accurate timing
  for (let clipIndex = 0; clipIndex < project.clips.length; clipIndex++) {
    const clip = project.clips[clipIndex];
    const wordBoundaries = allWordBoundaries[clipIndex];
    const speechDuration = getClipDurationFromBoundaries(wordBoundaries);
    // Extend clip if any media needs more time after its trigger word.
    const mediaRequiredDuration = (clip.media || []).reduce((maxDuration: number, media: any) => {
      if (typeof media.duration !== 'number') return maxDuration;
      const localStart = findWordStartTime(wordBoundaries, media.words);
      return Math.max(maxDuration, localStart + media.duration);
    }, 0);
    const clipDuration = Math.max(speechDuration, mediaRequiredDuration);
    const clipStartTime = globalTime;
    const clipEndTime = clipStartTime + clipDuration;
    
    clipDurations.push(clipDuration);
    clipStartTimes.push(clipStartTime);
    
    // Process each media item in the clip
    (clip.media || []).forEach((media: any, mediaIndex: number) => {
      const localStart = findWordStartTime(wordBoundaries, media.words);
      const duration = media.duration || 1;
      const startTime = clipStartTime + localStart;
      const defaultEnd = startTime + duration;
      const stayInClip = media.stayInClip ?? (typeof media.stay === 'number' ? media.stay > 0 : false);
      const endTime = stayInClip ? clipEndTime : defaultEnd;
      
      mediaItems.push({
        id: `${clipIndex}-${mediaIndex}`,
        src: `${basePath}/${media.src}`,
        startTime,
        endTime,
        duration,
        words: media.words || '',
        clipIndex,
        mediaIndex,
        transitionIn: media.transitionIn,
        transitionDuration: media.transitionDuration,
        stayInClip,
        clipStartTime,
        clipEndTime
      });
    });
    
    globalTime += clipDuration;
  }
  
  // Sort by start time
  mediaItems.sort((a, b) => a.startTime - b.startTime);
  
  console.log('[Timeline] Complete timeline calculated:', {
    totalItems: mediaItems.length,
    totalDuration: globalTime,
    clipDurations,
    clipStartTimes,
    mediaItems: mediaItems.map(m => ({
      id: m.id,
      src: m.src.split('/').pop(),
      startTime: m.startTime.toFixed(2),
      endTime: m.endTime.toFixed(2),
      words: m.words
    }))
  });
  
  return {
    mediaItems,
    totalDuration: globalTime,
    clipDurations,
    clipStartTimes
  };
}

/**
 * Synchronous version with estimated timing for immediate use
 */
export function calculateEstimatedTimeline(project: any): PlaybackTimeline {
  const projectName = project.name;
  const basePath = `/projects/${projectName}/footage`;
  const mediaItems: MediaItem[] = [];
  const clipDurations: number[] = [];
  const clipStartTimes: number[] = [];
  
  let globalTime = 0;
  
  project.clips.forEach((clip: any, clipIndex: number) => {
    const words = (clip.speech || '').split(/\s+/).filter((w: string) => w.length > 0);
    const speechDuration = Math.max(2, words.length * 0.5);
    const mediaRequiredDuration = (clip.media || []).reduce((maxDuration: number, media: any) => {
      if (typeof media.duration !== 'number') return maxDuration;

      let estimatedStartTime = 0;
      if (media.words) {
        const triggerWords = media.words.trim().split(/\s+/);
        const firstWord = triggerWords[0].toLowerCase().replace(/[^a-z0-9]/g, '');
        const wordIndex = words.findIndex((w: string) =>
          w.toLowerCase().replace(/[^a-z0-9]/g, '') === firstWord
        );
        if (wordIndex !== -1) {
          estimatedStartTime = wordIndex * 0.5;
        }
      }

      return Math.max(maxDuration, estimatedStartTime + media.duration);
    }, 0);
    const clipDuration = Math.max(speechDuration, mediaRequiredDuration);
    const clipStartTime = globalTime;
    const clipEndTime = clipStartTime + clipDuration;
    
    clipDurations.push(clipDuration);
    clipStartTimes.push(clipStartTime);
    
    (clip.media || []).forEach((media: any, mediaIndex: number) => {
      // Estimate start time based on word position
      let estimatedStartTime = 0;
      if (media.words) {
        const triggerWords = media.words.trim().split(/\s+/);
        const firstWord = triggerWords[0].toLowerCase().replace(/[^a-z0-9]/g, '');
        const wordIndex = words.findIndex((w: string) =>
          w.toLowerCase().replace(/[^a-z0-9]/g, '') === firstWord
        );
        if (wordIndex !== -1) {
          estimatedStartTime = wordIndex * 0.5;
        }
      }
      
      const duration = media.duration || 1;
      const startTime = clipStartTime + estimatedStartTime;
      const defaultEnd = startTime + duration;
      const stayInClip = media.stayInClip ?? (typeof media.stay === 'number' ? media.stay > 0 : false);
      const endTime = stayInClip ? clipEndTime : defaultEnd;
      
      mediaItems.push({
        id: `${clipIndex}-${mediaIndex}`,
        src: `${basePath}/${media.src}`,
        startTime,
        endTime,
        duration,
        words: media.words || '',
        clipIndex,
        mediaIndex,
        transitionIn: media.transitionIn,
        transitionDuration: media.transitionDuration,
        stayInClip,
        clipStartTime,
        clipEndTime
      });
    });
    
    globalTime += clipDuration;
  });
  
  // Sort by start time
  mediaItems.sort((a, b) => a.startTime - b.startTime);
  
  return {
    mediaItems,
    totalDuration: globalTime,
    clipDurations,
    clipStartTimes
  };
}

/**
 * Get current active media based on global time from pre-calculated timeline
 */
export function getCurrentMediaFromTimeline(timeline: PlaybackTimeline, globalTime: number): MediaItem | null {
  // Find the media that should be active at this time
  for (const media of timeline.mediaItems) {
    if (globalTime >= media.startTime && globalTime < media.endTime) {
      return media;
    }
  }
  
  // If no media is active, return the last media that has started
  let lastStartedMedia: MediaItem | null = null;
  for (const media of timeline.mediaItems) {
    if (media.startTime <= globalTime) {
      lastStartedMedia = media;
    } else {
      break;
    }
  }
  
  return lastStartedMedia;
}

/**
 * Get clip index and local time from global time
 */
export function getClipPositionFromGlobalTime(timeline: PlaybackTimeline, globalTime: number): { clipIndex: number, localTime: number } {
  let accumulated = 0;
  
  for (let i = 0; i < timeline.clipDurations.length; i++) {
    const clipDuration = timeline.clipDurations[i];
    
    if (globalTime < accumulated + clipDuration) {
      return {
        clipIndex: i,
        localTime: globalTime - accumulated
      };
    }
    
    accumulated += clipDuration;
  }
  
  // If beyond all clips, return last clip
  const lastClipIndex = timeline.clipDurations.length - 1;
  return {
    clipIndex: lastClipIndex,
    localTime: timeline.clipDurations[lastClipIndex]
  };
}

/**
 * Get global time from clip position
 */
export function getGlobalTimeFromClipPosition(timeline: PlaybackTimeline, clipIndex: number, localTime: number): number {
  let accumulated = 0;
  
  for (let i = 0; i < clipIndex; i++) {
    accumulated += timeline.clipDurations[i];
  }
  
  return accumulated + localTime;
}

/**
 * Seek to specific time and return clip position
 */
export function seekToTime(timeline: PlaybackTimeline, targetTime: number): { clipIndex: number, localTime: number } {
  const clampedTime = Math.max(0, Math.min(targetTime, timeline.totalDuration));
  return getClipPositionFromGlobalTime(timeline, clampedTime);
}

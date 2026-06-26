export async function generateAudio(projectId: string): Promise<{ success: boolean; message?: string; error?: string }> {
  try {
    console.log('[generateAudio] Starting API call for project:', projectId);
    
    const response = await fetch('/api/generate-audio', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ projectId })
    });

    console.log('[generateAudio] API response status:', response.status);
    
    const result = await response.json();
    console.log('[generateAudio] API response data:', result);
    
    if (!response.ok || !result.success) {
      throw new Error(result.error || 'Audio generation failed');
    }
    
    return { success: true, message: result.message };
  } catch (error: any) {
    console.error('[generateAudio] API call failed:', error);
    return { success: false, error: error.message };
  }
}

export async function loadAudioFiles(projectId: string, speechClips: any[]): Promise<Map<string, HTMLAudioElement>> {
  const audioCache = new Map<string, HTMLAudioElement>();
  
  const loadPromises = speechClips.map(async (_: any, index: number) => {
    const audioPath = `/projects/${projectId}/audio/${index}.mp3`;
    
    try {
      const response = await fetch(audioPath);
      if (!response.ok) {
        throw new Error(`Failed to load ${audioPath}`);
      }

      const blob = await response.blob();
      const objectUrl = URL.createObjectURL(blob);
      const audio = new Audio(objectUrl);

      await new Promise<void>((resolve, reject) => {
        audio.onloadedmetadata = () => resolve();
        audio.onerror = () => reject(new Error(`Failed to load audio ${index}`));
      });

      const cacheKey = `${projectId}-${index}`;
      audioCache.set(cacheKey, audio);
      console.log(`[loadAudioFiles] Loaded ${audioPath} (${audio.duration.toFixed(2)}s)`);
      
      return audio;
    } catch (error) {
      console.error(`[loadAudioFiles] Error loading ${audioPath}:`, error);
      throw error;
    }
  });

  await Promise.all(loadPromises);
  return audioCache;
}

export async function checkAudioExists(projectId: string, speechClips: any[]): Promise<boolean> {
  try {
    console.log(`[checkAudioExists] Checking ${speechClips.length} audio files for project:`, projectId);
    
    // Check all audio files exist
    for (let i = 0; i < speechClips.length; i++) {
      const testUrl = `/projects/${projectId}/audio/${i}.mp3`;
      console.log(`[checkAudioExists] Checking file ${i}:`, testUrl);
      
      try {
        const response = await fetch(testUrl, { method: 'HEAD' });
        const contentType = response.headers.get('content-type');
        console.log(`[checkAudioExists] File ${i} status:`, response.status, 'Content-Type:', contentType);
        
        // Check if it's actually an audio file, not HTML fallback
        if (!response.ok || !contentType || !contentType.includes('audio')) {
          console.log(`[checkAudioExists] File ${i} missing or not audio (status: ${response.status}, type: ${contentType}), audio generation needed`);
          return false;
        }
      } catch (fetchError) {
        console.log(`[checkAudioExists] File ${i} fetch failed:`, fetchError);
        return false;
      }
    }
    
    console.log('[checkAudioExists] All audio files exist');
    return true;
  } catch (error) {
    console.log('[checkAudioExists] Error:', error);
    return false;
  }
}

export function getSpeechClips(project: any): any[] {
  return project.clips.filter((c: any) => 
    c.type !== 'transition' && typeof c?.speech === 'string' && c.speech.trim().length > 0
  );
}
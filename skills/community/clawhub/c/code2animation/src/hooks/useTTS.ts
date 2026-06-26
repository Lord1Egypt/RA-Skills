import { useState, useEffect, useRef, useCallback } from 'react';
import { AudioAlignment, VideoClip } from '@/types';

interface UseTTSProps {
  clip?: VideoClip;
  projectId?: string;
  clipIndex?: number;
  preloadedAudio?: HTMLAudioElement;
  onWordBoundary?: (word: string) => void;
  onEnd?: () => void;
}

export function useTTS({ clip, projectId, clipIndex, preloadedAudio, onWordBoundary, onEnd }: UseTTSProps = {}) {
  const [alignment, setAlignment] = useState<AudioAlignment | null>(null);
  const [duration, setDuration] = useState(0);
  const [audio, setAudio] = useState<HTMLAudioElement | null>(null);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const onWordBoundaryRef = useRef(onWordBoundary);
  const onEndRef = useRef(onEnd);
  const currentUrlRef = useRef<string | null>(null);

  useEffect(() => {
    onWordBoundaryRef.current = onWordBoundary;
    onEndRef.current = onEnd;
  }, [onWordBoundary, onEnd]);

  const stop = useCallback(() => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
    }
    setIsSpeaking(false);
  }, []);

  const cleanup = useCallback(() => {
    stop();
    // Don't revoke preloaded audio URLs
    if (currentUrlRef.current && !preloadedAudio) {
      URL.revokeObjectURL(currentUrlRef.current);
      currentUrlRef.current = null;
    }
    if (audioRef.current && !preloadedAudio) {
      audioRef.current.src = '';
      audioRef.current = null;
    }
    if (!preloadedAudio) {
      setAudio(null);
      setAlignment(null);
      setDuration(0);
    }
  }, [stop, preloadedAudio]);

  const loadResource = useCallback(async (pId: string, cIdx: number, speech?: string, options?: { voice?: string }) => {
    let isMounted = true;
    let objectUrl: string | null = null;

    try {
      if (!speech || !speech.trim()) return null;

      setIsLoading(true);
      cleanup(); // Clean up previous resources

      const audioPath = `/projects/${pId}/audio/${cIdx}.mp3`;
      const jsonPath = `/projects/${pId}/audio/${cIdx}.json`;

      console.log(`[useTTS] Loading audio from ${audioPath}`);

      // Try to load static audio file
      const audioRes = await fetch(audioPath);
      if (audioRes.ok && !isMounted) return null;

      if (audioRes.ok) {
        const blob = await audioRes.blob();
        objectUrl = URL.createObjectURL(blob);
        
        const newAudio = new Audio(objectUrl);
        
        await new Promise<void>((resolve, reject) => {
          newAudio.onloadedmetadata = () => {
            if (!isMounted) {
              reject(new Error('Component unmounted'));
              return;
            }
            resolve();
          };
          newAudio.onerror = () => reject(new Error('Audio load failed'));
        });

        if (!isMounted) return null;

        setDuration(newAudio.duration);
        setAudio(newAudio);
        audioRef.current = newAudio;
        currentUrlRef.current = objectUrl;

        // Load metadata for word boundaries
        try {
          const metaRes = await fetch(jsonPath);
          if (metaRes.ok) {
            const data = await metaRes.json();
            const parsedAlignment: AudioAlignment = {
              characters: [],
              character_start_times_seconds: [],
              character_end_times_seconds: []
            };

            if (Array.isArray(data)) {
              data.forEach((item: any) => {
                // Handle the nested structure: item.Metadata[0].Data
                if (item.Metadata && Array.isArray(item.Metadata) && item.Metadata.length > 0) {
                  const metadata = item.Metadata[0];
                  if (metadata.Type === 'WordBoundary' && metadata.Data) {
                    const start = metadata.Data.Offset / 10000000; // Convert from 100ns to seconds
                    const dur = metadata.Data.Duration / 10000000;
                    const text = metadata.Data.text?.Text || '';
                    
                    if (text) {
                      parsedAlignment.characters.push(text);
                      parsedAlignment.character_start_times_seconds.push(start);
                      parsedAlignment.character_end_times_seconds.push(start + dur);
                    }
                  }
                }
              });

              if (isMounted && parsedAlignment.characters.length > 0) {
                setAlignment(parsedAlignment);
                console.log(`[useTTS] Loaded ${parsedAlignment.characters.length} word boundaries`);
                
                // Set up word boundary tracking
                newAudio.ontimeupdate = () => {
                  if (onWordBoundaryRef.current && parsedAlignment.characters.length > 0) {
                    const currentTime = newAudio.currentTime;
                    const wordIndex = parsedAlignment.character_start_times_seconds.findIndex((startTime, i) => {
                      const endTime = parsedAlignment.character_end_times_seconds[i];
                      return currentTime >= startTime && currentTime < endTime;
                    });
                    
                    if (wordIndex >= 0) {
                      const word = parsedAlignment.characters[wordIndex];
                      if (word) onWordBoundaryRef.current(word);
                    }
                  }
                };
              }
            }
          }
        } catch (metaErr) {
          console.warn('[useTTS] Failed to load metadata:', metaErr);
        }

        // Set up end handler
        newAudio.onended = () => {
          setIsSpeaking(false);
          onEndRef.current?.();
        };

        console.log(`[useTTS] Audio loaded successfully, duration: ${newAudio.duration}s`);
        return newAudio;
      } else {
        // If static file doesn't exist, try generating via TTS API
        console.log(`[useTTS] Static audio not found, trying TTS generation...`);
        
        const ttsResponse = await fetch('/api/tts', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            text: speech,
            voice: options?.voice,
            rate: '+0%',
            pitch: '+0Hz'
          })
        });

        if (ttsResponse.ok && isMounted) {
          const audioBlob = await ttsResponse.blob();
          objectUrl = URL.createObjectURL(audioBlob);
          
          const newAudio = new Audio(objectUrl);
          
          await new Promise<void>((resolve, reject) => {
            newAudio.onloadedmetadata = () => {
              if (!isMounted) {
                reject(new Error('Component unmounted'));
                return;
              }
              resolve();
            };
            newAudio.onerror = () => reject(new Error('TTS Audio load failed'));
          });

          if (!isMounted) return null;

          setDuration(newAudio.duration);
          setAudio(newAudio);
          audioRef.current = newAudio;
          currentUrlRef.current = objectUrl;

          newAudio.onended = () => {
            setIsSpeaking(false);
            onEndRef.current?.();
          };

          console.log(`[useTTS] TTS audio generated successfully, duration: ${newAudio.duration}s`);
          return newAudio;
        }
      }

      throw new Error('Failed to load or generate audio');

    } catch (error) {
      console.error('[useTTS] Error loading audio:', error);
      if (objectUrl) {
        URL.revokeObjectURL(objectUrl);
      }
      return null;
    } finally {
      if (isMounted) {
        setIsLoading(false);
      }
      return () => {
        isMounted = false;
      };
    }
  }, [cleanup]);

  const speak = useCallback(async () => {
    if (!audioRef.current) return false;
    
    try {
      setIsSpeaking(true);
      audioRef.current.currentTime = 0;
      await audioRef.current.play();
      return true;
    } catch (error) {
      console.error('[useTTS] Error playing audio:', error);
      setIsSpeaking(false);
      return false;
    }
  }, []);

  const pause = useCallback(() => {
    if (audioRef.current) {
      audioRef.current.pause();
      setIsSpeaking(false);
    }
  }, []);

  const resume = useCallback(async () => {
    if (!audioRef.current) return false;
    
    try {
      setIsSpeaking(true);
      await audioRef.current.play();
      return true;
    } catch (error) {
      console.error('[useTTS] Error resuming audio:', error);
      setIsSpeaking(false);
      return false;
    }
  }, []);

  // Auto-load when clip changes
  useEffect(() => {
    // If we have preloaded audio, use it directly
    if (preloadedAudio && clipIndex !== undefined) {
      console.log(`[useTTS] Using preloaded audio for clip ${clipIndex}`);
      setAudio(preloadedAudio);
      audioRef.current = preloadedAudio;
      setDuration(preloadedAudio.duration);
      
      // Set up end handler
      preloadedAudio.onended = () => {
        setIsSpeaking(false);
        onEndRef.current?.();
      };
      
      // Try to load metadata
      if (projectId !== undefined && clipIndex !== undefined) {
        const jsonPath = `/projects/${projectId}/audio/${clipIndex}.json`;
        fetch(jsonPath)
          .then(res => res.ok ? res.json() : null)
          .then(data => {
            if (data && Array.isArray(data)) {
              const parsedAlignment: AudioAlignment = {
                characters: [],
                character_start_times_seconds: [],
                character_end_times_seconds: []
              };

              data.forEach((item: any) => {
                // Handle the nested structure: item.Metadata[0].Data
                if (item.Metadata && Array.isArray(item.Metadata) && item.Metadata.length > 0) {
                  const metadata = item.Metadata[0];
                  if (metadata.Type === 'WordBoundary' && metadata.Data) {
                    const start = metadata.Data.Offset / 10000000;
                    const dur = metadata.Data.Duration / 10000000;
                    const text = metadata.Data.text?.Text || '';
                    
                    if (text) {
                      parsedAlignment.characters.push(text);
                      parsedAlignment.character_start_times_seconds.push(start);
                      parsedAlignment.character_end_times_seconds.push(start + dur);
                    }
                  }
                }
              });

              if (parsedAlignment.characters.length > 0) {
                setAlignment(parsedAlignment);
                console.log(`[useTTS] Loaded ${parsedAlignment.characters.length} word boundaries for preloaded audio`);
                
                // Set up word boundary tracking
                preloadedAudio.ontimeupdate = () => {
                  if (onWordBoundaryRef.current && parsedAlignment.characters.length > 0) {
                    const currentTime = preloadedAudio.currentTime;
                    const wordIndex = parsedAlignment.character_start_times_seconds.findIndex((startTime, i) => {
                      const endTime = parsedAlignment.character_end_times_seconds[i];
                      return currentTime >= startTime && currentTime < endTime;
                    });
                    
                    if (wordIndex >= 0) {
                      const word = parsedAlignment.characters[wordIndex];
                      if (word) onWordBoundaryRef.current(word);
                    }
                  }
                };
              }
            }
          })
          .catch(err => console.warn('[useTTS] Failed to load metadata:', err));
      }
      
      return;
    }
    
    // Fallback to loading audio if not preloaded
    if (projectId !== undefined && clipIndex !== undefined && clip?.speech) {
      loadResource(projectId, clipIndex, clip.speech, { voice: clip.voice });
    }
  }, [projectId, clipIndex, clip?.speech, clip?.voice, preloadedAudio, loadResource]);

  // Cleanup on unmount
  useEffect(() => {
    return cleanup;
  }, [cleanup]);

  return {
    alignment,
    duration,
    audio,
    isSpeaking,
    isLoading,
    speak,
    pause,
    resume,
    stop,
    loadResource,
    cleanup
  };
}
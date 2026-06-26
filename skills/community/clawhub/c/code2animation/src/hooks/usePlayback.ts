import { useState, useEffect, useRef } from 'react';

export function usePlayback(processedClips: any[]) {
  const [currentClipIndex, setCurrentClipIndex] = useState(0);
  const [currentTime, setCurrentTime] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [resetCounter, setResetCounter] = useState(0);

  const requestRef = useRef<number>(0);
  const previousTimeRef = useRef<number | undefined>(undefined);
  const isPlayingRef = useRef(isPlaying);

  useEffect(() => {
    isPlayingRef.current = isPlaying;
  }, [isPlaying]);

  const animate = (time: number) => {
    if (previousTimeRef.current != undefined && isPlayingRef.current) {
      const deltaTime = (time - previousTimeRef.current) / 1000;
      setCurrentTime((prevTime: number) => prevTime + deltaTime);
    }
    previousTimeRef.current = time;
    if (isPlayingRef.current) {
      requestRef.current = requestAnimationFrame(animate);
    }
  };

  useEffect(() => {
    if (isPlaying) {
      previousTimeRef.current = performance.now();
      requestRef.current = requestAnimationFrame(animate);
    } else {
      cancelAnimationFrame(requestRef.current);
      previousTimeRef.current = undefined;
    }
    return () => cancelAnimationFrame(requestRef.current);
  }, [isPlaying]);

  const nextClip = () => {
    if (currentClipIndex < processedClips.length - 1) {
      const nextIndex = currentClipIndex + 1;
      setCurrentClipIndex(nextIndex);
      setCurrentTime(0);
    }
  };

  const prevClip = () => {
    if (currentClipIndex > 0) {
      const prevIndex = currentClipIndex - 1;
      setCurrentClipIndex(prevIndex);
      setCurrentTime(0);
    } else {
      setCurrentTime(0);
      setResetCounter((c) => c + 1);
    }
  };

  const reset = () => {
    setCurrentClipIndex(0);
    setCurrentTime(0);
    setIsPlaying(false);
    setResetCounter((c: number) => c + 1);
  };

  return {
    currentClipIndex,
    setCurrentClipIndex,
    currentTime,
    setCurrentTime,
    isPlaying,
    setIsPlaying,
    resetCounter,
    nextClip,
    prevClip,
    reset
  };
}
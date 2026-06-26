// Typewriter animation handler
export class TypewriterHandler {
  constructor(core) {
    this.core = core;
  }
  
  handleTypewriterAnimation(callback, delay) {
    console.log('[Animation] Setting up typewriter animation');
    const id = this.core.nextTaskId++;
    const callbackStr = callback.toString();
    
    // Schedule the start of typewriter effect
    this.core.addTask(() => {
      console.log('[Animation] Starting typewriter effect');
      
      // Handle different typewriter patterns
      if (callbackStr.includes('streamText')) {
        this.handleStreamingText();
      } else {
        this.handleStandardTypewriter();
      }
    }, delay, 'timeout');
    
    return id;
  }
  
  handleStreamingText() {
    // Complex streaming text (agentsaas_complex_task.html)
    const promptEl = document.getElementById('prompt');
    if (promptEl) {
      const targetText = "Analyze Nvidia valuation and recent earnings reports to generate a comprehensive investment summary.";
      
      window.registerFrameAnimation(promptEl, (frame, elapsed) => {
        const charTime = 0.03; // 30ms per character
        const expectedChars = Math.floor(elapsed / charTime);
        
        if (expectedChars <= targetText.length) {
          promptEl.innerHTML = targetText.substring(0, expectedChars);
          console.log(`[Animation] Streaming: "${promptEl.innerHTML.substring(-10)}"`);
        }
      }, targetText.length * 0.03 + 1);
    }
  }
  
  handleStandardTypewriter() {
    // Standard typewriter (agentsaas_intro_text.html)
    const brandEl = document.getElementById('brand-text');
    if (brandEl) {
      const targetText = "AgentSaaS Computer";
      
      window.registerFrameAnimation(brandEl, (frame, elapsed) => {
        const charTime = 0.04; // 40ms per character
        const expectedChars = Math.floor(elapsed / charTime);
        
        if (expectedChars <= targetText.length) {
          brandEl.innerHTML = targetText.substring(0, expectedChars);
          console.log(`[Animation] Typewriter: "${brandEl.innerHTML}"`);
        }
      }, targetText.length * 0.04 + 1);
    }
  }
}
// Special effects like explosions
export class EffectsManager {
  constructor() {}
  
  createExplosion() {
    console.log('[Animation] Creating explosion effect');
    const ptcContainer = document.getElementById('particles');
    if (!ptcContainer) return;
    
    // Create particles with frame-based animation
    for (let i = 0; i < 60; i++) {
      const el = document.createElement('div');
      el.className = 'particle';
      
      const angle = Math.random() * Math.PI * 2;
      const distOuter = 800 + Math.random() * 400;
      
      ptcContainer.appendChild(el);
      
      // Register frame-based particle animation
      window.registerFrameAnimation(el, (frame, elapsed) => {
        if (elapsed >= 0.05) { // 50ms delay
          const animTime = elapsed - 0.05;
          
          if (animTime <= 1) {
            // Expand phase
            el.style.opacity = '1';
            const progress = animTime;
            const x = Math.cos(angle) * distOuter * progress;
            const y = Math.sin(angle) * distOuter * progress;
            const z = Math.random() * 500 * progress;
            el.style.transform = `translate3d(${x}px, ${y}px, ${z}px)`;
          } else if (animTime <= 2) {
            // Contract phase
            const contractProgress = animTime - 1;
            el.style.opacity = 1 - contractProgress;
            el.style.transform = 'translate3d(0,0,0)';
          } else {
            // Remove element
            if (el.parentNode) {
              el.parentNode.removeChild(el);
            }
          }
        }
      }, 2.1);
    }
    
    // Create icons with frame-based animation
    const icons = ['✨', '🚀', '🧠', '⚡', '🌐', '📊'];
    for (let i = 0; i < 15; i++) {
      const el = document.createElement('div');
      el.className = 'icon';
      el.innerHTML = icons[i % icons.length];
      
      const angle = Math.random() * Math.PI * 2;
      const dist = 600 + Math.random() * 300;
      
      el.style.transform = `translate3d(${Math.cos(angle) * dist}px, ${Math.sin(angle) * dist}px, -200px) scale(0)`;
      ptcContainer.appendChild(el);
      
      // Register frame-based icon animation
      window.registerFrameAnimation(el, (frame, elapsed) => {
        const startTime = 0.2 + i * 0.05;
        if (elapsed >= startTime) {
          const animTime = elapsed - startTime;
          
          if (animTime <= 1.5) {
            // Appear and move
            el.style.opacity = '1';
            const progress = Math.min(animTime / 1.5, 1);
            const x = Math.cos(angle) * (dist / 3) * progress;
            const y = Math.sin(angle) * (dist / 3) * progress;
            const rotation = (Math.random() * 60 - 30) * progress;
            el.style.transform = `translate3d(${x}px, ${y}px, 0) scale(${progress}) rotate(${rotation}deg)`;
          } else if (animTime <= 2) {
            // Fade out
            const fadeProgress = (animTime - 1.5) / 0.5;
            el.style.opacity = 1 - fadeProgress;
            el.style.transform = 'translate3d(0,0,0) scale(0)';
          } else {
            // Remove element
            if (el.parentNode) {
              el.parentNode.removeChild(el);
            }
          }
        }
      }, 2.1);
    }
  }
}
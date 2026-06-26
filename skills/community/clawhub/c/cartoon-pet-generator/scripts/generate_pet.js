#!/usr/bin/env node

const fs = require('fs');
const { execSync } = require('child_process');

// Parse arguments
const args = process.argv.slice(2);
const petType = args[0] || 'dog';
const outputPath = args[1] || '/tmp/pet.png';

// Parse options
const options = {};
for (let i = 2; i < args.length; i += 2) {
  const key = args[i].replace(/^--/, '');
  const value = args[i + 1];
  options[key] = value;
}

// Default colors
const defaults = {
  dog: { body: '#D2691E', ear: '#8B4513', nose: '#000000', bg: '#87CEEB' },
  cat: { body: '#FFB347', ear: '#FF8C00', nose: '#FF69B4', bg: '#E6E6FA' },
  rabbit: { body: '#FFFFFF', ear: '#FFB6C1', nose: '#FF69B4', bg: '#98FB98' },
  bear: { body: '#8B4513', ear: '#654321', nose: '#000000', bg: '#F5DEB3' }
};

const colors = {
  body: options['body-color'] || defaults[petType]?.body || '#D2691E',
  ear: options['ear-color'] || defaults[petType]?.ear || '#8B4513',
  nose: options['nose-color'] || defaults[petType]?.nose || '#000000',
  bg: options['bg-color'] || defaults[petType]?.bg || '#87CEEB'
};

const size = parseInt(options['size']) || 400;

// Pet generators
const pets = {
  dog: (colors, size) => `
<svg width='${size}' height='${size}' xmlns='http://www.w3.org/2000/svg'>
  <rect width='${size}' height='${size}' fill='${colors.bg}'/>

  <!-- Body -->
  <ellipse cx='${size/2}' cy='${size*0.63}' rx='${size*0.25}' ry='${size*0.175}' fill='${colors.body}' stroke='${colors.ear}' stroke-width='3'/>

  <!-- Head -->
  <ellipse cx='${size*0.525}' cy='${size*0.35}' rx='${size*0.175}' ry='${size*0.15}' fill='${colors.body}' stroke='${colors.ear}' stroke-width='3'/>

  <!-- Ears -->
  <ellipse cx='${size*0.36}' cy='${size*0.24}' rx='${size*0.06}' ry='${size*0.088}' fill='${colors.ear}' stroke='${colors.ear}' stroke-width='2'/>
  <ellipse cx='${size*0.69}' cy='${size*0.24}' rx='${size*0.06}' ry='${size*0.088}' fill='${colors.ear}' stroke='${colors.ear}' stroke-width='2'/>

  <!-- Eyes -->
  <ellipse cx='${size*0.45}' cy='${size*0.325}' rx='${size*0.038}' ry='${size*0.038}' fill='white' stroke='black' stroke-width='2'/>
  <ellipse cx='${size*0.6}' cy='${size*0.325}' rx='${size*0.038}' ry='${size*0.038}' fill='white' stroke='black' stroke-width='2'/>

  <!-- Pupils -->
  <ellipse cx='${size*0.462}' cy='${size*0.33}' rx='${size*0.018}' ry='${size*0.018}' fill='black'/>
  <ellipse cx='${size*0.612}' cy='${size*0.33}' rx='${size*0.018}' ry='${size*0.018}' fill='black'/>

  <!-- Eye highlights -->
  <ellipse cx='${size*0.47}' cy='${size*0.325}' rx='${size*0.008}' ry='${size*0.008}' fill='white'/>
  <ellipse cx='${size*0.62}' cy='${size*0.325}' rx='${size*0.008}' ry='${size*0.008}' fill='white'/>

  <!-- Nose -->
  <ellipse cx='${size*0.525}' cy='${size*0.4}' rx='${size*0.038}' ry='${size*0.025}' fill='${colors.nose}'/>

  <!-- Mouth -->
  <path d='M ${size*0.46} ${size*0.425} A ${size*0.063} ${size*0.063} 0 0 0 ${size*0.59} ${size*0.425}' stroke='${colors.ear}' stroke-width='3' fill='none'/>

  <!-- Tongue -->
  <ellipse cx='${size*0.525}' cy='${size*0.475}' rx='${size*0.025}' ry='${size*0.038}' fill='#FF69B4'/>

  <!-- Legs -->
  <ellipse cx='${size*0.325}' cy='${size*0.775}' rx='${size*0.05}' ry='${size*0.075}' fill='${colors.body}' stroke='${colors.ear}' stroke-width='2'/>
  <ellipse cx='${size*0.675}' cy='${size*0.775}' rx='${size*0.05}' ry='${size*0.075}' fill='${colors.body}' stroke='${colors.ear}' stroke-width='2'/>

  <!-- Tail -->
  <path d='M ${size*0.725} ${size*0.55} Q ${size*0.825} ${size*0.5} ${size*0.85} ${size*0.65}' stroke='${colors.ear}' stroke-width='8' fill='none' stroke-linecap='round'/>
</svg>`,

  cat: (colors, size) => `
<svg width='${size}' height='${size}' xmlns='http://www.w3.org/2000/svg'>
  <rect width='${size}' height='${size}' fill='${colors.bg}'/>

  <!-- Body -->
  <ellipse cx='${size/2}' cy='${size*0.63}' rx='${size*0.25}' ry='${size*0.175}' fill='${colors.body}' stroke='${colors.ear}' stroke-width='3'/>

  <!-- Head -->
  <ellipse cx='${size/2}' cy='${size*0.35}' rx='${size*0.175}' ry='${size*0.15}' fill='${colors.body}' stroke='${colors.ear}' stroke-width='3'/>

  <!-- Ears (triangular) -->
  <polygon points='${size*0.33},${size*0.28} ${size*0.28},${size*0.12} ${size*0.4},${size*0.22}' fill='${colors.ear}' stroke='${colors.ear}' stroke-width='2'/>
  <polygon points='${size*0.67},${size*0.28} ${size*0.72},${size*0.12} ${size*0.6},${size*0.22}' fill='${colors.ear}' stroke='${colors.ear}' stroke-width='2'/>

  <!-- Eyes (cat style) -->
  <ellipse cx='${size*0.42}' cy='${size*0.325}' rx='${size*0.038}' ry='${size*0.05}' fill='#90EE90' stroke='black' stroke-width='2'/>
  <ellipse cx='${size*0.58}' cy='${size*0.325}' rx='${size*0.038}' ry='${size*0.05}' fill='#90EE90' stroke='black' stroke-width='2'/>

  <!-- Pupils (vertical) -->
  <ellipse cx='${size*0.42}' cy='${size*0.325}' rx='${size*0.01}' ry='${size*0.03}' fill='black'/>
  <ellipse cx='${size*0.58}' cy='${size*0.325}' rx='${size*0.01}' ry='${size*0.03}' fill='black'/>

  <!-- Nose (heart shape) -->
  <path d='M ${size*0.5} ${size*0.39} L ${size*0.485} ${size*0.375} A ${size*0.015} ${size*0.015} 0 0 1 ${size*0.5} ${size*0.36} A ${size*0.015} ${size*0.015} 0 0 1 ${size*0.515} ${size*0.375} Z' fill='${colors.nose}'/>

  <!-- Whiskers -->
  <line x1='${size*0.3}' y1='${size*0.38}' x2='${size*0.4}' y2='${size*0.39}' stroke='#666' stroke-width='1.5'/>
  <line x1='${size*0.3}' y1='${size*0.41}' x2='${size*0.4}' y2='${size*0.4}' stroke='#666' stroke-width='1.5'/>
  <line x1='${size*0.6}' y1='${size*0.39}' x2='${size*0.7}' y2='${size*0.38}' stroke='#666' stroke-width='1.5'/>
  <line x1='${size*0.6}' y1='${size*0.4}' x2='${size*0.7}' y2='${size*0.41}' stroke='#666' stroke-width='1.5'/>

  <!-- Mouth -->
  <path d='M ${size*0.47} ${size*0.42} Q ${size*0.5} ${size*0.44} ${size*0.53} ${size*0.42}' stroke='${colors.ear}' stroke-width='2' fill='none'/>

  <!-- Legs -->
  <ellipse cx='${size*0.35}' cy='${size*0.775}' rx='${size*0.05}' ry='${size*0.075}' fill='${colors.body}' stroke='${colors.ear}' stroke-width='2'/>
  <ellipse cx='${size*0.65}' cy='${size*0.775}' rx='${size*0.05}' ry='${size*0.075}' fill='${colors.body}' stroke='${colors.ear}' stroke-width='2'/>

  <!-- Tail -->
  <path d='M ${size*0.75} ${size*0.63} Q ${size*0.85} ${size*0.5} ${size*0.8} ${size*0.4}' stroke='${colors.body}' stroke-width='${size*0.05}' fill='none' stroke-linecap='round'/>
</svg>`,

  rabbit: (colors, size) => `
<svg width='${size}' height='${size}' xmlns='http://www.w3.org/2000/svg'>
  <rect width='${size}' height='${size}' fill='${colors.bg}'/>

  <!-- Body -->
  <ellipse cx='${size/2}' cy='${size*0.65}' rx='${size*0.25}' ry='${size*0.2}' fill='${colors.body}' stroke='#DDD' stroke-width='3'/>

  <!-- Head -->
  <ellipse cx='${size/2}' cy='${size*0.38}' rx='${size*0.175}' ry='${size*0.15}' fill='${colors.body}' stroke='#DDD' stroke-width='3'/>

  <!-- Long ears -->
  <ellipse cx='${size*0.38}' cy='${size*0.15}' rx='${size*0.045}' ry='${size*0.125}' fill='${colors.body}' stroke='#DDD' stroke-width='2'/>
  <ellipse cx='${size*0.38}' cy='${size*0.15}' rx='${size*0.025}' ry='${size*0.1}' fill='${colors.ear}'/>
  <ellipse cx='${size*0.62}' cy='${size*0.15}' rx='${size*0.045}' ry='${size*0.125}' fill='${colors.body}' stroke='#DDD' stroke-width='2'/>
  <ellipse cx='${size*0.62}' cy='${size*0.15}' rx='${size*0.025}' ry='${size*0.1}' fill='${colors.ear}'/>

  <!-- Eyes -->
  <ellipse cx='${size*0.43}' cy='${size*0.36}' rx='${size*0.038}' ry='${size*0.038}' fill='white' stroke='black' stroke-width='2'/>
  <ellipse cx='${size*0.57}' cy='${size*0.36}' rx='${size*0.038}' ry='${size*0.038}' fill='white' stroke='black' stroke-width='2'/>

  <!-- Pupils -->
  <ellipse cx='${size*0.44}' cy='${size*0.36}' rx='${size*0.015}' ry='${size*0.015}' fill='black'/>
  <ellipse cx='${size*0.58}' cy='${size*0.36}' rx='${size*0.015}' ry='${size*0.015}' fill='black'/>

  <!-- Nose -->
  <ellipse cx='${size/2}' cy='${size*0.42}' rx='${size*0.02}' ry='${size*0.015}' fill='${colors.nose}'/>

  <!-- Mouth -->
  <path d='M ${size*0.48} ${size*0.44} L ${size*0.5} ${size*0.46} L ${size*0.52} ${size*0.44}' stroke='#999' stroke-width='2' fill='none'/>

  <!-- Cheeks -->
  <ellipse cx='${size*0.35}' cy='${size*0.42}' rx='${size*0.038}' ry='${size*0.025}' fill='#FFB6C1' opacity='0.6'/>
  <ellipse cx='${size*0.65}' cy='${size*0.42}' rx='${size*0.038}' ry='${size*0.025}' fill='#FFB6C1' opacity='0.6'/>

  <!-- Legs -->
  <ellipse cx='${size*0.35}' cy='${size*0.82}' rx='${size*0.05}' ry='${size*0.063}' fill='${colors.body}' stroke='#DDD' stroke-width='2'/>
  <ellipse cx='${size*0.65}' cy='${size*0.82}' rx='${size*0.05}' ry='${size*0.063}' fill='${colors.body}' stroke='#DDD' stroke-width='2'/>
</svg>`,

  bear: (colors, size) => `
<svg width='${size}' height='${size}' xmlns='http://www.w3.org/2000/svg'>
  <rect width='${size}' height='${size}' fill='${colors.bg}'/>

  <!-- Body -->
  <ellipse cx='${size/2}' cy='${size*0.63}' rx='${size*0.3}' ry='${size*0.225}' fill='${colors.body}' stroke='${colors.ear}' stroke-width='3'/>

  <!-- Head -->
  <ellipse cx='${size/2}' cy='${size*0.35}' rx='${size*0.2}' ry='${size*0.175}' fill='${colors.body}' stroke='${colors.ear}' stroke-width='3'/>

  <!-- Ears (round) -->
  <circle cx='${size*0.32}' cy='${size*0.2}' r='${size*0.075}' fill='${colors.body}' stroke='${colors.ear}' stroke-width='2'/>
  <circle cx='${size*0.68}' cy='${size*0.2}' r='${size*0.075}' fill='${colors.body}' stroke='${colors.ear}' stroke-width='2'/>

  <!-- Inner ears -->
  <circle cx='${size*0.32}' cy='${size*0.2}' r='${size*0.04}' fill='#DEB887'/>
  <circle cx='${size*0.68}' cy='${size*0.2}' r='${size*0.04}' fill='#DEB887'/>

  <!-- Snout -->
  <ellipse cx='${size/2}' cy='${size*0.4}' rx='${size*0.088}' ry='${size*0.063}' fill='#DEB887'/>

  <!-- Eyes -->
  <circle cx='${size*0.4}' cy='${size*0.32}' r='${size*0.03}' fill='black'/>
  <circle cx='${size*0.6}' cy='${size*0.32}' r='${size*0.03}' fill='black'/>

  <!-- Eye highlights -->
  <circle cx='${size*0.408}' cy='${size*0.31}' r='${size*0.01}' fill='white'/>
  <circle cx='${size*0.608}' cy='${size*0.31}' r='${size*0.01}' fill='white'/>

  <!-- Nose -->
  <ellipse cx='${size/2}' cy='${size*0.38}' rx='${size*0.03}' ry='${size*0.02}' fill='${colors.nose}'/>

  <!-- Mouth -->
  <path d='M ${size*0.47} ${size*0.42} Q ${size*0.5} ${size*0.45} ${size*0.53} ${size*0.42}' stroke='#654321' stroke-width='2' fill='none'/>

  <!-- Belly -->
  <ellipse cx='${size/2}' cy='${size*0.65}' rx='${size*0.15}' ry='${size*0.125}' fill='#DEB887'/>

  <!-- Legs -->
  <ellipse cx='${size*0.3}' cy='${size*0.82}' rx='${size*0.075}' ry='${size*0.1}' fill='${colors.body}' stroke='${colors.ear}' stroke-width='2'/>
  <ellipse cx='${size*0.7}' cy='${size*0.82}' rx='${size*0.075}' ry='${size*0.1}' fill='${colors.body}' stroke='${colors.ear}' stroke-width='2'/>

  <!-- Paws -->
  <ellipse cx='${size*0.3}' cy='${size*0.88}' rx='${size*0.05}' ry='${size*0.03}' fill='#DEB887'/>
  <ellipse cx='${size*0.7}' cy='${size*0.88}' rx='${size*0.05}' ry='${size*0.03}' fill='#DEB887'/>
</svg>`
};

// Generate SVG
const svgGenerator = pets[petType];
if (!svgGenerator) {
  console.error(`Unknown pet type: ${petType}`);
  console.error(`Available types: ${Object.keys(pets).join(', ')}`);
  process.exit(1);
}

const svg = svgGenerator(colors, size);
const svgPath = outputPath.replace('.png', '.svg');

// Write SVG
fs.writeFileSync(svgPath, svg);

// Convert to PNG
try {
  // Try rsvg-convert first
  execSync(`rsvg-convert "${svgPath}" -o "${outputPath}"`, { stdio: 'inherit' });
  console.log(`PNG created: ${outputPath}`);
} catch (e) {
  // Fall back to ImageMagick
  try {
    execSync(`convert "${svgPath}" "${outputPath}"`, { stdio: 'inherit' });
    console.log(`PNG created: ${outputPath}`);
  } catch (e2) {
    console.error('Failed to convert SVG to PNG. Please install rsvg-convert or ImageMagick.');
    console.error(`SVG file is available at: ${svgPath}`);
    process.exit(1);
  }
}

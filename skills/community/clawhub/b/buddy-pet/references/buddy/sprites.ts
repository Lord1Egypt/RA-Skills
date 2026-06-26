/**
 * BUDDY ASCII Sprites - Complete 18 Species
 * Reference: Claude Code src/buddy/sprites.ts
 * 
 * Each sprite is 5 rows x 12 characters
 * Each species has 3 frames: idle, fidget, special
 */

import type { Species } from './types';

export interface SpriteFrames {
  idle: string[];
  fidget: string[];
  special: string[];
}

export type SpriteSheet = Record<Species, SpriteFrames>;

// Full sprite sheet for all 18 species - Claude Code authentic sprites
const SPRITE_SHEET: SpriteSheet = {
  // 🐙 OCTOPUS - 小墨's species
  octopus: {
    idle: [
      '   ▄▄▄▄   ',
      '  (·◉·)  ',
      ' >( ═══ )<',
      '  ══════  ',
      '     UU   ',
    ],
    fidget: [
      '   ▄▄▄▄   ',
      '  (·◉·)  ',
      ' >( ═══ )<',
      '  ══════  ',
      '    ∪∪    ',
    ],
    special: [
      '   ∪∪∪∪   ',
      '  (·◉·)  ',
      ' >( ═══ )<',
      '  ══════  ',
      '    ∪∪    ',
    ],
  },

  // 🦆 DUCK
  duck: {
    idle: [
      '  ___  ',
      ' =(o)=  ',
      '  /   >',
      ' <    |',
      '  ‾‾‾  ',
    ],
    fidget: [
      '  ___  ',
      ' =(o)=  ',
      '  /   >',
      ' <    |',
      '  ‾‾‾  ',
    ],
    special: [
      '  ___  ',
      ' =(o)=  ',
      '  W   >',
      ' <    |',
      '  ‾‾‾  ',
    ],
  },

  // 🪿 GOOSE
  goose: {
    idle: [
      '  ~~~ ',
      ' =(O)= ',
      '  /   >',
      ' <    |',
      '  ‾‾‾  ',
    ],
    fidget: [
      '  ~~~ ',
      ' =(O)= ',
      '  /   >',
      ' <    |',
      '  ‾‾‾  ',
    ],
    special: [
      '  ~~~ ',
      ' =(O)= ',
      '  G   >',
      ' <    |',
      '  ‾‾‾  ',
    ],
  },

  // 🐱 CAT
  cat: {
    idle: [
      ' =·ω·= ',
      ' (·◉·) ',
      ' >(   )<',
      '  ═══  ',
      '     UU',
    ],
    fidget: [
      ' =·ω·= ',
      ' (·◉·) ',
      ' >(   )<',
      '  ═══  ',
      '    ∪∪',
    ],
    special: [
      ' =·ω·= ',
      ' (·◉·) ',
      ' >(   )<',
      '  ═══  ',
      '   ∪∪ ',
    ],
  },

  // 🐉 DRAGON
  dragon: {
    idle: [
      '  ///  ',
      ' =(◉◉)= ',
      ' >(  m)<',
      '  ///// ',
      '    UU  ',
    ],
    fidget: [
      '  ///  ',
      ' =(◉◉)= ',
      ' >(  m)<',
      '  ///// ',
      '   ∪∪  ',
    ],
    special: [
      '  ///  ',
      ' =(◉◉)= ',
      ' >(  M)<',
      '  ///// ',
      '   ∪∪  ',
    ],
  },

  // 🦉 OWL
  owl: {
    idle: [
      '  ???  ',
      ' (·◉·) ',
      ' >(   )<',
      '  /‾‾\\ ',
      '     UU',
    ],
    fidget: [
      '  ???  ',
      ' (·◉·) ',
      ' >(   )<',
      '  /‾‾\\ ',
      '   ∪∪  ',
    ],
    special: [
      '  ???  ',
      ' (·◉·) ',
      ' >(   )<',
      '  /‾‾\\ ',
      '  ∪∪ ∪∪',
    ],
  },

  // 🐧 PENGUIN
  penguin: {
    idle: [
      '  ___  ',
      ' /(o)\\ ',
      ' >(   )<',
      '  \\___/ ',
      '     UU',
    ],
    fidget: [
      '  ___  ',
      ' /(o)\\ ',
      ' >(   )<',
      '  \\___/ ',
      '   ∪∪  ',
    ],
    special: [
      '  ___  ',
      ' /(O)\\ ',
      ' >(   )<',
      '  \\___/ ',
      '  ∪∪ ∪∪',
    ],
  },

  // 🐢 TURTLE
  turtle: {
    idle: [
      '  ~~~~  ',
      ' ( @@@ )',
      ' >(    )',
      '  ~~~~~~',
      '     UU ',
    ],
    fidget: [
      '  ~~~~  ',
      ' ( @@@ )',
      ' >(    )',
      '  ~~~~~~',
      '    ∪∪ ',
    ],
    special: [
      '  ~~~~  ',
      ' ( @@@ )',
      ' >(    )',
      '  ~~~~~~',
      '   ∪∪  ',
    ],
  },

  // 🐌 SNAIL
  snail: {
    idle: [
      ' @@@@  ',
      ' (··)  ',
      '  )   )',
      ' <____>',
      '     UU',
    ],
    fidget: [
      ' @@@@  ',
      ' (··)  ',
      '  )   )',
      ' <____>',
      '    ∪∪',
    ],
    special: [
      ' @@@@  ',
      ' (··)  ',
      '  S   )',
      ' <____>',
      '   ∪∪  ',
    ],
  },

  // 👻 GHOST
  ghost: {
    idle: [
      ' ~~~~  ',
      '(·  ·) ',
      '<(    )>',
      '  ‾‾‾‾ ',
      '   UU  ',
    ],
    fidget: [
      ' ~~~~  ',
      '(·  ·) ',
      '<(    )>',
      '  ‾‾‾‾ ',
      '  ∪∪   ',
    ],
    special: [
      ' ~~~~  ',
      '(·  ·) ',
      '<( G  )>',
      '  ‾‾‾‾ ',
      ' ∪∪ ∪∪ ',
    ],
  },

  // 🦎 AXOLOTL
  axolotl: {
    idle: [
      ' ~‿~  ',
      ' (·◉·) ',
      ' >(   )<',
      '  /~~~\\',
      '     UU',
    ],
    fidget: [
      ' ~‿~  ',
      ' (·◉·) ',
      ' >(   )<',
      '  /~~~\\',
      '   ∪∪  ',
    ],
    special: [
      ' ~‿~  ',
      ' (·◉·) ',
      ' >( A )<',
      '  /~~~\\',
      '  ∪∪ ∪∪',
    ],
  },

  // 🦫 CAPYBARA
  capybara: {
    idle: [
      '  ~~~  ',
      ' =(·◉·)=',
      ' >(    )<',
      '  ~~~~~ ',
      '     UU ',
    ],
    fidget: [
      '  ~~~  ',
      ' =(·◉·)=',
      ' >(    )<',
      '  ~~~~~ ',
      '   ∪∪   ',
    ],
    special: [
      '  ~~~  ',
      ' =(·◉·)=',
      ' >( C )<',
      '  ~~~~~ ',
      ' ∪∪   ∪∪',
    ],
  },

  // 🌵 CACTUS
  cactus: {
    idle: [
      '  \|/  ',
      '  \|/  ',
      ' ( + ) ',
      '  /|\\  ',
      '     UU',
    ],
    fidget: [
      '  \|/  ',
      '  \|/  ',
      ' ( + ) ',
      '  /|\\  ',
      '   ∪∪  ',
    ],
    special: [
      '  \\|/  ',
      '  \\|/  ',
      ' ( + ) ',
      '  /|\\  ',
      '  ∪∪ ∪∪',
    ],
  },

  // 🤖 ROBOT
  robot: {
    idle: [
      ' [===] ',
      ' (·◉·) ',
      ' >(   )<',
      '  [===] ',
      '     UU',
    ],
    fidget: [
      ' [===] ',
      ' (·◉·) ',
      ' >(   )<',
      '  [===] ',
      '   ∪∪  ',
    ],
    special: [
      ' [===] ',
      ' (·◉·) ',
      ' >( R )<',
      '  [===] ',
      '  ∪∪ ∪∪',
    ],
  },

  // 🐰 RABBIT
  rabbit: {
    idle: [
      ' (··)  ',
      ' (·◉·) ',
      ' >(   )<',
      '  /___\\',
      '     UU',
    ],
    fidget: [
      ' (··)  ',
      ' (·◉·) ',
      ' >(   )<',
      '  /___\\',
      '   ∪∪  ',
    ],
    special: [
      ' (··)  ',
      ' (·◉·) ',
      ' >( R )<',
      '  /___\\',
      '  ∪∪ ∪∪',
    ],
  },

  // 🍄 MUSHROOM
  mushroom: {
    idle: [
      ' ~~~~  ',
      ' (..)  ',
      '  )(  ',
      ' /    )',
      '     UU',
    ],
    fidget: [
      ' ~~~~  ',
      ' (..)  ',
      '  )(  ',
      ' /    )',
      '   ∪∪  ',
    ],
    special: [
      ' ~~~~  ',
      ' (MM)  ',
      '  )(  ',
      ' /    )',
      ' ∪∪  ∪∪',
    ],
  },

  // 🐈 CHONK
  chonk: {
    idle: [
      ' =·ω·= ',
      ' (·◉·) ',
      ' >(   )<',
      '  ~~~~~',
      '     UU',
    ],
    fidget: [
      ' =·ω·= ',
      ' (·◉·) ',
      ' >(   )<',
      '  ~~~~~',
      '   ∪∪  ',
    ],
    special: [
      ' =·ω·= ',
      ' (·◉·) ',
      ' >( C )<',
      '  ~~~~~',
      ' ∪∪ ∪∪',
    ],
  },

  // 🫧 BLOB
  blob: {
    idle: [
      ' ~~~~  ',
      ' (·◉·) ',
      ' >(   )<',
      '  ~~~~  ',
      '     UU',
    ],
    fidget: [
      ' ~~~~  ',
      ' (·◉·) ',
      ' >(   )<',
      '  ~~~~  ',
      '   ∪∪  ',
    ],
    special: [
      ' ~~~~  ',
      ' (·◉·) ',
      ' >( B )<',
      '  ~~~~  ',
      ' ∪∪ ∪∪',
    ],
  },
};

// Animation frame sequence (15 frames)
const FRAME_SEQUENCE = [0, 0, 0, 0, 1, 0, 0, 0, -1, 0, 0, 2, 0, 0, 0];

// Get sprite for a species
export function getSprite(species: Species): SpriteFrames {
  return SPRITE_SHEET[species] || SPRITE_SHEET.blob;
}

// Get current animation frame
export function getAnimationFrame(frameIndex: number): 'idle' | 'fidget' | 'special' {
  const frame = FRAME_SEQUENCE[frameIndex % FRAME_SEQUENCE.length];
  if (frame === 1) return 'fidget';
  if (frame === 2) return 'special';
  return 'idle';
}

// Render sprite with optional eye replacement (for blink -1)
export function renderSprite(species: Species, frame: 'idle' | 'fidget' | 'special', blink = false): string[] {
  const sprite = getSprite(species);
  const lines = [...sprite[frame]];
  
  if (blink && frame === 'idle') {
    // Replace eyes with '-' for blink effect
    lines[1] = lines[1].replace(/[·✦×◉@°]/g, '-');
  }
  
  return lines;
}

// Compact mode for narrow terminals (< 100 cols)
export function getCompactFace(species: Species): string {
  const faces: Record<Species, string> = {
    octopus: '=·ω·=',
    duck: '(·>',
    goose: '(·>',
    cat: '=^.^=',
    dragon: '(◉◠)',
    owl: 'òᴥó',
    penguin: '>°<',
    turtle: '-_-',
    snail: '@~@',
    ghost: '(-.-)',
    axolotl: '~◉~',
    capybara: '=·ω·=',
    cactus: '√√√',
    robot: '[·_·]',
    rabbit: '=·ω·=',
    mushroom: '=·ω·=',
    chonk: '=·ᴗ·=',
    blob: '=·~·=',
  };
  return faces[species] || '=·?·=';
}

// Render pet with optional hat
export function renderPetWithHat(species: Species, hat: string, frameIndex = 0): string[] {
  const frame = getAnimationFrame(frameIndex);
  const lines = renderSprite(species, frame);
  
  if (hat === 'none') return lines;
  
  const hatLines: Record<string, string[]> = {
    crown:    ['  ♔♔♔  ', '  ═════'],
    wizard:   ['  /\\_\\  ', '  /   '],
    tophat:   ['  ___  ', '  [___]'],
    beanie:   ['  ~~~  ', '  ~~~~~'],
    propeller: ['  ●    ', '  |    '],
    halo:     ['   ○   ', '  ═══  '],
    tinyduck: ['  🦆  ', '  ~~~  '],
  };
  
  const h = hatLines[hat] || [];
  if (h.length >= 2) {
    lines[0] = h[0];
    lines[1] = h[1] + lines[1].slice(h[1].length);
  }
  
  return lines;
}

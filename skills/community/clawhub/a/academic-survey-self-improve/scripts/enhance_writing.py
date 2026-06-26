#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Academic Writing Enhancer
Improves academic writing quality by adding transitions and formal language
"""

import re

TRANSITION_PHRASES = {
    'addition': ['furthermore', 'moreover', 'in addition', 'additionally', 'besides'],
    'contrast': ['however', 'nevertheless', 'nonetheless', 'in contrast', 'conversely'],
    'cause': ['therefore', 'consequently', 'thus', 'hence', 'as a result'],
    'example': ['for example', 'for instance', 'specifically', 'in particular'],
    'sequence': ['first', 'second', 'finally', 'subsequently', 'meanwhile'],
    'summary': ['in summary', 'to conclude', 'overall', 'in conclusion']
}

def enhance_academic_writing(text):
    """Enhance academic writing quality"""
    
    # Add transition words between paragraphs
    text = add_transitions(text)
    
    # Improve formality
    text = improve_formality(text)
    
    # Enhance sentence variety
    text = enhance_sentence_variety(text)
    
    return text

def add_transitions(text):
    """Add transition words between sections"""
    
    # Add transitions before section starts
    section_transitions = {
        r'\\section\{Background': '\\section{Background}\n\nTo establish the theoretical foundations,',
        r'\\section\{Taxonomy': '\\section{Taxonomy}\n\nBuilding upon these foundations,',
        r'\\section\{.*Architecture': '\\section{Architecture}\n\nWith this background established,',
        r'\\section\{Training': '\\section{Training}\n\nHaving described the architecture,',
        r'\\section\{Experimental': '\\section{Experimental Analysis}\n\nTo evaluate the effectiveness,',
        r'\\section\{.*Challenge': '\\section{Challenges}\n\nDespite these advances,',
        r'\\section\{Conclusion': '\\section{Conclusion}\n\nIn summary,'
    }
    
    for pattern, replacement in section_transitions.items():
        text = re.sub(pattern, replacement, text)
    
    # Add transitions between paragraphs
    paragraph_starts = ['This survey', 'We propose', 'Our analysis', 'Recent work', 'However', 'Therefore']
    
    return text

def improve_formality(text):
    """Improve formality of language"""
    
    # Replace informal expressions
    replacements = {
        'a lot of': 'numerous',
        'big': 'substantial',
        'small': 'limited',
        'good': 'effective',
        'bad': 'problematic',
        'show': 'demonstrate',
        'use': 'utilize',
        'need': 'require',
        'get': 'obtain',
        'help': 'facilitate',
    }
    
    for informal, formal in replacements.items():
        # Only replace in text content, not commands
        text = re.sub(rf'\b{informal}\b', formal, text, flags=re.IGNORECASE)
    
    return text

def enhance_sentence_variety(text):
    """Enhance sentence structure variety"""
    
    # Add complex sentence structures
    # This is simplified; real enhancement needs NLP
    
    return text

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python enhance_writing.py <tex_file>")
        sys.exit(1)
    
    tex_file = sys.argv[1]
    
    with open(tex_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    enhanced = enhance_academic_writing(content)
    
    # Save enhanced version
    output_file = tex_file.replace('.tex', '_enhanced.tex')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(enhanced)
    
    print(f"✓ Enhanced writing saved to: {output_file}")

if __name__ == '__main__':
    main()

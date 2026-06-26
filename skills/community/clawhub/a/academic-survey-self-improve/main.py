#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Academic Survey Self-Improve - Main Entry Point
Unified interface for survey generation, evaluation, and improvement
"""

import sys
import argparse
from pathlib import Path

def generate_survey(topic=None, output_dir=None, from_arxiv=False, smart=False, auto=False, quality=False):
    """Generate academic survey"""
    if output_dir is None:
        output_dir = Path(__file__).parent / 'output'
    
    if quality:
        from quality_generator import QualitySurveyGenerator
        generator = QualitySurveyGenerator(output_dir)
        result = generator.generate_with_quality_control()
    elif auto:
        from fully_automated_generator import FullyAutomatedSurveyGenerator
        generator = FullyAutomatedSurveyGenerator(output_dir)
        result = generator.generate_fully_automated()
    elif smart:
        from smart_generator import SmartArXivGenerator
        generator = SmartArXivGenerator(output_dir)
        result = generator.generate_hourly_survey()
    elif from_arxiv:
        from arxiv_generator import ArXivSurveyGenerator
        generator = ArXivSurveyGenerator(output_dir)
        result = generator.generate_from_arxiv(topic)
    else:
        from generator import GenericSurveyGenerator
        generator = GenericSurveyGenerator(output_dir)
        result = generator.generate(topic)
    
    if result:
        print(f"✅ Survey generated: {result['tex_file']}")
        print(f"📄 Output: {output_dir}")
        if 'novelty_score' in result:
            print(f"🎯 Novelty score: {result['novelty_score']}/10")
        if 'quality' in result:
            print(f"📊 Quality: {result['quality']['score']}/10 ({result['quality']['pages']} pages, {result['quality']['references']} refs)")
        print(f"📊 Estimated quality: {result.get('estimated_score', 'N/A')}/10")
    return result

def evaluate_survey(pdf_path):
    """Evaluate survey quality using LLM"""
    from evaluator import LLMEvaluator
    
    # Convert PDF path to TEX path
    tex_path = str(pdf_path).replace('.pdf', '.tex')
    
    evaluator = LLMEvaluator()
    result = evaluator.evaluate(tex_path)
    
    print(f"\n{'='*60}")
    print(f"Overall Score: {result['overall_score']}/10")
    print(f"{'='*60}")
    
    for dim, score in result['dimension_scores'].items():
        print(f"  {dim}: {score}/10")
    
    print(f"\nMetrics:")
    for key, value in result['metrics'].items():
        print(f"  {key}: {value}")
    
    if result.get('feedback'):
        print(f"\nFeedback:")
        for fb in result['feedback']:
            print(f"  {fb}")
    
    return result

def improve_survey(pdf_path, target_score=None):
    """Run LLM-guided improvement cycle"""
    from improver import LLMImprover
    
    # Convert PDF path to TEX path
    tex_path = str(pdf_path).replace('.pdf', '.tex')
    
    if target_score is None:
        target_score = 8.0
    
    improver = LLMImprover()
    result = improver.improve(tex_path, target_score)
    
    print(f"\n{'='*60}")
    print(f"✅ Improvement complete!")
    print(f"{'='*60}")
    print(f"Initial: {result['initial_score']}/10")
    print(f"Final: {result['final_score']}/10")
    print(f"Improvement: +{result['improvement']:.2f}")
    print(f"Iterations: {result['iterations']}")
    
    return result

def auto_generate(topic, target_score=8.0):
    """Auto generate and improve until target using LLM"""
    print(f"🚀 Auto-generating survey: {topic}")
    print(f"Target score: {target_score}/10\n")
    
    # Generate high-quality survey in one pass
    result = generate_survey(topic, quality='high')
    pdf_path = result['pdf_file']
    
    # Evaluate
    print(f"\n{'='*60}")
    print("Evaluating generated survey...")
    eval_result = evaluate_survey(pdf_path)
    current_score = eval_result['overall_score']
    
    # Only improve if below target
    if current_score < target_score:
        print(f"\nCurrent: {current_score}/10, Target: {target_score}/10")
        print("Running LLM-guided improvement...")
        improve_result = improve_survey(pdf_path, target_score)
        current_score = improve_result['final_score']
    else:
        print(f"✅ Already at target: {current_score}/10")
    
    print(f"\n🎉 Final score: {current_score}/10")
    return pdf_path

def main():
    parser = argparse.ArgumentParser(description='Academic Survey Self-Improve')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate survey')
    gen_parser.add_argument('topic', type=str, nargs='?', help='Survey topic (optional if --smart, --auto, or --quality)')
    gen_parser.add_argument('--output', type=str, help='Output directory')
    gen_parser.add_argument('--from-arxiv', action='store_true', help='Search arXiv and generate from papers')
    gen_parser.add_argument('--smart', action='store_true', help='Auto-select hottest topic from arXiv')
    gen_parser.add_argument('--auto', action='store_true', help='Fully automated: search, identify novel topic, check for duplicates, generate')
    gen_parser.add_argument('--quality', action='store_true', help='High-quality generation with quality control (6-8 pages, 40+ references)')
    
    # Evaluate command
    eval_parser = subparsers.add_parser('evaluate', help='Evaluate survey')
    eval_parser.add_argument('pdf', type=str, help='PDF file to evaluate')
    
    # Improve command
    imp_parser = subparsers.add_parser('improve', help='Improve survey')
    imp_parser.add_argument('pdf', type=str, help='PDF file to improve')
    imp_parser.add_argument('--target', type=float, help='Target score')
    
    # Auto command
    auto_parser = subparsers.add_parser('auto', help='Auto generate and improve')
    auto_parser.add_argument('topic', type=str, help='Survey topic')
    auto_parser.add_argument('--target', type=float, default=8.0, help='Target score')
    
    args = parser.parse_args()
    
    if args.command == 'generate':
        generate_survey(args.topic if args.topic else None, args.output, 
                       from_arxiv=args.from_arxiv, smart=args.smart, 
                       auto=args.auto, quality=args.quality)
    elif args.command == 'evaluate':
        evaluate_survey(args.pdf)
    elif args.command == 'improve':
        improve_survey(args.pdf, args.target)
    elif args.command == 'auto':
        auto_generate(args.topic, args.target)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()

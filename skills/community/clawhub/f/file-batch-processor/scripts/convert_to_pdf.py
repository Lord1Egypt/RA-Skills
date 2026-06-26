#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch File to PDF Converter Tool
Supports converting images and text files to PDF
"""

import os
import sys
import argparse
from PIL import Image
from fpdf import FPDF
import PyPDF2

def convert_to_pdf(folder_path, output_folder=None, dry_run=False):
    """
    Batch convert files to PDF
    
    Args:
        folder_path: Source folder path
        output_folder: Output folder path (default: same as source folder)
        dry_run: Whether to preview only without execution
    """
    if not os.path.exists(folder_path):
        print(f"Error: Folder does not exist {folder_path}")
        return False
    
    if output_folder is None:
        output_folder = folder_path
    
    # Create output folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Supported source file formats
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
    text_extensions = ['.txt', '.md']
    
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    convertible_files = [f for f in files if os.path.splitext(f)[1].lower() in image_extensions + text_extensions]
    
    if not convertible_files:
        print("Warning: No convertible files found in the folder")
        return True
    
    print(f"Found {len(convertible_files)} convertible files, preparing to convert to PDF...")
    
    converted_count = 0
    for filename in convertible_files:
        old_path = os.path.join(folder_path, filename)
        name, ext = os.path.splitext(filename)
        
        # Generate PDF filename
        pdf_filename = f"{name}.pdf"
        pdf_path = os.path.join(output_folder, pdf_filename)
        
        try:
            if dry_run:
                print(f"Preview: {filename} → {pdf_filename}")
            else:
                if ext.lower() in image_extensions:
                    # Image to PDF
                    with Image.open(old_path) as img:
                        # Create PDF
                        pdf = FPDF()
                        pdf.add_page()
                        
                        # Calculate appropriate size
                        width, height = img.size
                        max_width = 200  # mm
                        max_height = 280  # mm
                        
                        if width > height:
                            new_width = max_width
                            new_height = height * (max_width / width)
                        else:
                            new_height = max_height
                            new_width = width * (max_height / height)
                        
                        # Resize image and save to PDF
                        img.save('temp_image.jpg', quality=95)
                        pdf.image('temp_image.jpg', x=(210-new_width)/2, y=(297-new_height)/2, 
                                 w=new_width, h=new_height)
                        pdf.output(pdf_path)
                        os.remove('temp_image.jpg')
                        
                elif ext.lower() in text_extensions:
                    # Text to PDF
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=12)
                    
                    # Read text file
                    with open(old_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    
                    # Add text to PDF
                    for line in lines:
                        pdf.cell(200, 10, txt=line.rstrip(), ln=True)
                    
                    pdf.output(pdf_path)
                
                print(f"Converted: {filename} → {pdf_filename}")
                converted_count += 1
                
        except Exception as e:
            print(f"Conversion failed {filename}: {e}")
    
    print(f"Complete! Total {converted_count} files converted to PDF")
    return True

def main():
    parser = argparse.ArgumentParser(description='Batch File to PDF Converter Tool')
    parser.add_argument('folder', help='Folder path to process')
    parser.add_argument('--output', help='Output folder path (default: same as source folder)')
    parser.add_argument('--dry-run', action='store_true', help='Preview only without execution')
    
    args = parser.parse_args()
    
    convert_to_pdf(
        folder_path=args.folder,
        output_folder=args.output,
        dry_run=args.dry_run
    )

if __name__ == "__main__":
    main()
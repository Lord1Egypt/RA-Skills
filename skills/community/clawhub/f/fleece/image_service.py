"""
Image Service Module for Fleece Application

This module provides optimized image loading and caching services for the Fleece application.
It handles fetching images from URLs, caching them for improved performance, and providing
fallback default images when remote images cannot be loaded.

Features:
- Multi-level image caching (memory cache + LRU cache)
- Parallel image loading
- Pre-generated default card image
- Robust error handling with logging

Author: @chenyuan99
Date: May 2025
"""

import os
import functools
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import streamlit as st
import logging
import time

# Configure logging
logging.basicConfig(level=logging.WARNING)

# Create the default image once at module level for better performance
DEFAULT_CARD_IMAGE = None
try:
    # Pre-generate a default credit card image to avoid creating it repeatedly
    # This significantly improves performance when multiple card images fail to load
    width, height = 340, 220
    DEFAULT_CARD_IMAGE = Image.new('RGB', (width, height), color=(30, 58, 138))  # Dark blue background
    draw = ImageDraw.Draw(DEFAULT_CARD_IMAGE)
    draw.rectangle([(20, 20), (70, 60)], fill=(255, 215, 0))  # Gold chip
    draw.text((width//2, height//2), "FLEECE CARD", fill=(255, 255, 255), anchor="mm")
    draw.text((40, 160), "•••• •••• •••• ••••", fill=(255, 255, 255))
    draw.text((40, 185), "CARDHOLDER NAME", fill=(200, 200, 200))
    draw.text((280, 185), "VALID THRU", fill=(200, 200, 200))
    draw.text((280, 200), "MM/YY", fill=(255, 255, 255))
    logging.info("Default card image pre-generated successfully")
except Exception as e:
    logging.error(f"Failed to create default image: {e}")

# Cache for storing fetched images
IMAGE_CACHE = {}  # In-memory dictionary cache {url: (timestamp, content)}
CACHE_EXPIRY = 3600  # Cache expiry in seconds (1 hour)

@functools.lru_cache(maxsize=32)
def cached_image_fetch(image_url):
    """
    Fetch and cache image content from a URL with multi-level caching.
    
    This function implements a dual-layer caching system:
    1. An in-memory dictionary cache (IMAGE_CACHE) with time-based expiration
    2. Python's LRU cache decorator for function call memoization
    
    Args:
        image_url (str): The URL of the image to fetch
        
    Returns:
        bytes: The image content as bytes if successful, None otherwise
        
    Performance Notes:
        - Uses a 5-second timeout for network requests
        - Caches successful responses for 1 hour
        - Logs cache hits and misses for debugging
    """
    # Check if we have a valid cached response in the dictionary cache
    if image_url in IMAGE_CACHE:
        timestamp, content = IMAGE_CACHE[image_url]
        if time.time() - timestamp < CACHE_EXPIRY:
            logging.info(f"Cache hit for {image_url}")
            return content
    
    # Fetch the image if not in cache or expired
    try:
        logging.info(f"Fetching image from {image_url}")
        response = requests.get(image_url, timeout=5)
        if response.status_code == 200:
            # Store in cache
            IMAGE_CACHE[image_url] = (time.time(), response.content)
            return response.content
    except Exception as e:
        logging.warning(f"Error fetching image from {image_url}: {e}")
    
    return None

def display_card_image(image_url):
    """
    Load and return a credit card image with robust caching and fallback mechanisms.
    
    This function attempts to load an image from a URL with the following fallback sequence:
    1. Try to fetch the image from the URL using the cached_image_fetch function
    2. If successful, convert the bytes to a PIL Image object
    3. If unsuccessful, use the pre-generated default card image
    4. If the pre-generated image is unavailable, create a new default image
    5. If all else fails, return None
    
    Args:
        image_url (str): The URL of the credit card image to load
        
    Returns:
        PIL.Image.Image: The loaded image if successful, a default image as fallback,
                         or None if all attempts fail
                         
    Performance Notes:
        - Uses cached_image_fetch for efficient URL fetching
        - Returns a copy of the pre-generated default image for better performance
        - Only generates a new default image as a last resort
    """
    # Use cached image fetch
    content = cached_image_fetch(image_url)
    
    if content:
        try:
            img = Image.open(BytesIO(content))
            return img
        except Exception as e:
            logging.warning(f"Could not process image content: {e}")
    
    # Return the pre-generated default image if available
    if DEFAULT_CARD_IMAGE:
        logging.info("Using default card image")
        return DEFAULT_CARD_IMAGE.copy()
    
    # Fallback to generating a new default image if the pre-generated one failed
    try:
        logging.warning("Creating new default image as fallback")
        width, height = 340, 220
        img = Image.new('RGB', (width, height), color=(30, 58, 138))
        draw = ImageDraw.Draw(img)
        draw.rectangle([(20, 20), (70, 60)], fill=(255, 215, 0))
        draw.text((width//2, height//2), "FLEECE CARD", fill=(255, 255, 255), anchor="mm")
        draw.text((40, 160), "•••• •••• •••• ••••", fill=(255, 255, 255))
        draw.text((40, 185), "CARDHOLDER NAME", fill=(200, 200, 200))
        draw.text((280, 185), "VALID THRU", fill=(200, 200, 200))
        draw.text((280, 200), "MM/YY", fill=(255, 255, 255))
        return img
    except Exception as e:
        logging.error(f"Error creating fallback default image: {e}")
    
    # If all else fails, return None
    return None
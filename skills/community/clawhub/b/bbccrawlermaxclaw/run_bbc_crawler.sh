#!/bin/bash
echo "Starting BBC Crawler for BBC News..."
echo "This will crawl 5 pages of BBC News as a demo."
echo "Results will be saved in the 'data' folder."

# Ensure data directory exists
mkdir -p data

python3 universal_crawler_v2.py --url https://www.bbc.com/news --max-pages 5 --output data

if [ $? -ne 0 ]; then
    echo "Error running crawler. Please make sure you have run install_dependencies.sh first."
    exit 1
fi
echo "Crawl completed successfully! Check the 'data' folder."

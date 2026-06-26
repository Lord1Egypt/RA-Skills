"""
ChromaDB plugin test script
Verify all functionality works correctly
"""
import tempfile
import shutil
from chromadb_plugin import ChromaDBStore

def run_tests():
    print("==============================================")
    print("Running ChromaDB plugin tests...")
    print("==============================================")
    
    # Create temporary directory for test
    temp_dir = tempfile.mkdtemp()
    try:
        # Test 1: Initialize store
        print("[Test 1/6] Initializing ChromaDB store...")
        vs = ChromaDBStore(path=temp_dir, gpu_accelerate=False)
        print("✅ Store initialized successfully")
        
        # Test 2: Add documents
        print("[Test 2/6] Adding documents...")
        vs.add(
            texts=[
                "OpenClaw ChromaDB plugin supports hybrid search",
                "ChromaDB is faster than LanceDB for large datasets",
                "Memory evolution project uses vector search for knowledge retrieval"
            ],
            metadatas=[
                {"category": "plugin", "source": "docs"},
                {"category": "performance", "source": "benchmark"},
                {"category": "project", "source": "docs"}
            ],
            ids=["doc1", "doc2", "doc3"]
        )
        count = vs.count()
        assert count == 3, f"Expected 3 documents, got {count}"
        print(f"✅ {count} documents added successfully")
        
        # Test 3: Basic query
        print("[Test 3/6] Running basic query...")
        results = vs.query(query_texts=["hybrid search feature"], n_results=2)
        assert len(results["ids"][0]) == 2
        assert results["ids"][0][0] == "doc1"
        print("✅ Basic query works correctly")
        
        # Test 4: Filtered query
        print("[Test 4/6] Running filtered query...")
        results = vs.query(query_texts=["vector search"], n_results=5, where={"category": "project"})
        assert len(results["ids"][0]) == 1
        assert results["ids"][0][0] == "doc3"
        print("✅ Filtered query works correctly")
        
        # Test 5: Hybrid query
        print("[Test 5/6] Running hybrid query...")
        results = vs.hybrid_query(query_texts=["ChromaDB performance"], n_results=2)
        assert len(results["ids"][0]) == 2
        assert results["ids"][0][0] == "doc2"
        print("✅ Hybrid query works correctly")
        
        # Test 6: Delete document
        print("[Test 6/6] Deleting document...")
        vs.delete(ids=["doc1"])
        count = vs.count()
        assert count == 2
        print("✅ Document deleted successfully")
        
        print("==============================================")
        print("✅ All 6 tests passed! Plugin is working correctly")
        print("==============================================")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False
    finally:
        # Cleanup temp directory
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)

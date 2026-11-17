import importlib.util
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest

SPEC=importlib.util.spec_from_file_location('analysis_db',Path(__file__).resolve().parents[1]/'scripts/analysis_db.py')
db=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(db)

class CacheTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.path=str(Path(self.temp.name)/'cache.sqlite')
    def test_missing_cache_read_does_not_create_it(self):
        self.assertIsNone(db.status(self.path,1,'http://one:8080/#main','EPUB'))
        self.assertEqual(db.search(self.path,'x',10),[])
        self.assertFalse(Path(self.path).exists())
    def test_legacy_schema_is_preserved_not_overwritten(self):
        con=sqlite3.connect(self.path);con.execute('CREATE TABLE analyses (legacy TEXT)');con.execute("INSERT INTO analyses VALUES ('keep')");con.commit();con.close()
        before=Path(self.path).read_bytes()
        with self.assertRaises(ValueError):db.init_db(self.path)
        self.assertEqual(Path(self.path).read_bytes(),before)
    def test_language_and_endpoint_keys_do_not_collide(self):
        record={'book_id':1,'library_id':'http://one:8080/#main','title':'Fixture','format':'EPUB','file_hash':'sha256:'+'a'*64,'lang':'ja','summary':'summary','highlights':['one','two'],'reread':[],'tags':[],'coverage':{'mode':'full'}}
        db.upsert(self.path,record);db.upsert(self.path,{**record,'lang':'en'});db.upsert(self.path,{**record,'library_id':'http://two:8080/#main'})
        for endpoint,lang in [('http://one:8080/#main','ja'),('http://one:8080/#main','en'),('http://two:8080/#main','ja')]:
            result=db.status(self.path,1,endpoint,'EPUB',lang);self.assertEqual((result['library_id'],result['lang']),(endpoint,lang))
        self.assertEqual(len(db.search(self.path,'Fixture',10)),3)

if __name__=='__main__':unittest.main()
